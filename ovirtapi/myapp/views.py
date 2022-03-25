import urllib
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from . import config
from .decorations import unauthentification_user
from .models import *
from .func import *
from .forms import *
from requests.structures import CaseInsensitiveDict
from django.contrib.auth.decorators import login_required


@unauthentification_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    context = {}
    response = render(request, 'myapp/login.html', context)
    return response


@login_required(login_url='login')
def logout_User(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):  # отрисовка главной страницы
    usersvm = {}
    get_user_vm = {}
    get_user_vm = ResourcesProxmox.objects.filter(account=request.user)

    context = {'get_all_vm': get_user_vm, }

    if (request.POST):
        login_data = request.POST.dict()
        if 'stop' in login_data:
            uuid = request.POST['Numd']
            instance = ResourcesProxmox.objects.get(uuid=uuid)
            x = vmStop(proxmoxer_api(), instance.node, instance.vmid)
            y = check_status(proxmoxer_api(), instance.node, x)
            while y['status'] != "stopped":
                y = check_status(proxmoxer_api(), instance.node, x)

            y = check_status(proxmoxer_api(), instance.node, x)
            update_local_base()
            user_vm = ResourcesProxmox.objects.filter(account=request.user)
            context2 = {'get_all_vm': user_vm, }
            return render(request, 'myapp/index.html', context2)

        elif 'run' in login_data:
            uuid = request.POST['Numd']
            instance = ResourcesProxmox.objects.get(uuid=uuid)
            vmStart(proxmoxer_api(), instance.node, instance.vmid)
            update_local_base()
            return render(request, 'myapp/index.html', context)

        elif 'delete' in login_data:
            uuid = request.POST['Numd']
            instance = ResourcesProxmox.objects.get(uuid=uuid)
            deleteVm(proxmoxer_api(), instance.node, instance.vmid)
            instance.delete()
            return render(request, 'myapp/index.html', context)

        elif 'console' in login_data:
            uuid = request.POST['Vumd']
            instance = ResourcesProxmox.objects.get(uuid=uuid)
            vnclink = consoleLink(proxmoxer_api(), instance.node, instance.vmid)
            response = redirect(vnclink)
            ticket_cons = access_ticket()
            cookie_auth = urllib.parse.quote_plus(ticket_cons['ticket'])
            expiry_time = 60 * 60  # in seconds
            response.set_cookie("PVEAuthCookie", value=cookie_auth, expires=expiry_time, domain='.o0007.ru')

            return response
            # class ="btn btn-info" onclick="window.open(this.href, 'mywin', 'left=20,top=20,width=700,height=500,toolbar=0,resizable=1'); return false;" > console < / a > -->
    update_local_base()
    return render(request, 'myapp/index.html', context)


@login_required(login_url='login')
def profile(request):
    text = f"""
        Selected HttpRequest.user attributes:
        scheme: {request.scheme}
        path:   {request.path}
        method: {request.method}
        GET:    {request.GET}
        user:   {request.user}
        username:     {request.user.username}
        is_anonymous: {request.user.is_anonymous}
        is_staff:     {request.user.is_staff}
        is_superuser: {request.user.is_superuser}
        is_active:    {request.user.is_active}
    """

    get_user_vm = VirtMashID.objects.filter(account=request.user)
    all_vm = resources_get('vm')

    context = {'text': text, 'get_all_vm': get_user_vm}
    return render(request, 'myapp/profile.html', context)


@login_required(login_url='login')
def get_createvm(request):
    #     all_item = User_list.objects.get()
    #     body = get_vms_login(all_tem.name, all_item.password)
    form = CreatevmForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CreatevmForm(request.POST)
        if form.is_valid():
            vmid = nextWMID(proxmoxer_api())

            createVM(proxmoxer_api(), form.cleaned_data['name'], vmid, form.cleaned_data['maxmem'],
                     form.cleaned_data['maxdisk'],
                     form.cleaned_data['maxcpu'],
                     form.cleaned_data['iso'])
            newvm = form.save(commit=False)
            newvm.account = request.user
            newvm.vmid = vmid
            newvm = form.save()

            return redirect(index)
        else:
            form = CreatevmForm()

    return render(request, 'myapp/get_createvm.html', context)


@login_required(login_url='login')
def get_vm(request, uuid):
    vm = get_object_or_404(ResourcesProxmox, uuid=uuid)

    path = settings.MEDIA_ROOT
    list_node = (
        'loadavg', 'maxcpu', 'cpu', 'iowait', 'memtotal', 'memused', 'swaptotal', 'swapused', 'roottotal', 'rootused',
        'netin', 'netout')
    list_ds = ('maxcpu', 'cpu', 'maxmem', 'mem', 'maxdisk', 'disk', 'netin', 'netout', 'diskread', 'diskwrite')

    for i in list_ds:
        graf_png(i, vm.node, vm.vmid, uuid)

    img_list = os.listdir(path + '\\' + uuid)
    cdrom = get_config(proxmoxer_api(), vm.node, vm.vmid)
    if (request.POST):
        form = List_ISO(request.POST)
        if form.is_valid():
            print(form.cleaned_data['iso'])
            enablecdrom(proxmoxer_api(), vm.node, vm.vmid, form.cleaned_data['iso'])
        data = request.POST.dict()
        if 'disablecdrom' in data:
            disablecdrom(proxmoxer_api(), vm.node, vm.vmid)
        elif 'disablecdrom' in data:
            enablecdrom(proxmoxer_api(), vm.node, vm.vmid)

    formISO = List_ISO()

    context = {'vm': vm, "images": img_list, 'cdrom': cdrom, 'formISO': formISO, 'uuid': uuid}

    return render(request, 'myapp/vm.html', context)


@login_required(login_url='login')
def delete_vm(request, uuid):
    vm = get_object_or_404(ResourcesProxmox, uuid=uuid)
    login_user = request.user.username
    user_vm = vm.account
    context = {'vm.name': vm.name}
    if login_user == str(user_vm):
        deleteVm(proxmoxer_api(), vm.node, vm.vmid)
        vm.delete()
        # Redirect to a success page.

        return render(request, 'myapp/vm_delete.html', context)

    else:
        # Return an 'invalid login' error message.

        print("error")
        return redirect('index')


@login_required(login_url='login')
def stop_vm(request, uuid):
    vm = get_object_or_404(ResourcesProxmox, uuid=uuid)
    vmStop(proxmoxer_api(), vm.node, vm.vmid)
    return redirect('index')


@login_required(login_url='login')
def start_vm(request, uuid):
    vm = get_object_or_404(ResourcesProxmox, uuid=uuid)
    vmStart(proxmoxer_api(), vm.node, vm.vmid)
    return redirect('index')


@login_required(login_url='login')
def console_vm(request, uuid):
    instance = ResourcesProxmox.objects.get(uuid=uuid)
    vnclink = consoleLink(proxmoxer_api(), instance.node, instance.vmid)
    response = redirect(vnclink)
    ticket_cons = access_ticket()
    cookie_auth = urllib.parse.quote_plus(ticket_cons['ticket'])
    expiry_time = 60 * 60  # in seconds
    response.set_cookie("PVEAuthCookie", value=cookie_auth, expires=expiry_time, domain='.o0007.ru')
    return response

@login_required(login_url='login')
def get_template_vm(request):
    template_vm_list = {"debian9": 9000, "debian10": 9001, "ubuntu18": 9002, "ubuntu20": 9003, "ubuntu16": 9004,
                        "centos7": 9005}
    form = Template_form()
    if request.method == 'POST':
        templateVmOs = request.POST.get('templateVmOs')
        templateVmCPU = request.POST.get('templateVmCPU')
        templateVmMem = request.POST.get('templateVmMem')
        templateVmHDD = request.POST.get('templateVmHDD')
        vm_description = request.POST.get('vm_description')
        root_pass = request.POST.get('root_pass')
        clone_vm(template_vm_list[templateVmOs], vm_description, request.user, templateVmCPU, templateVmMem,
                 templateVmHDD, root_pass)
        # print(templateVmOs, templateVmCPU, templateVmMem, templateVmHDD)

        return redirect('index')

    context = {'form': form, }
    return render(request, 'myapp/vm_template.html', context)
