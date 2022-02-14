from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt

from . import config

from .decorations import unauthentification_user
from .models import *
from .func import *
from .forms import *
from requests.structures import CaseInsensitiveDict
import paramiko
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
    return render(request, 'myapp/login.html', context)


@login_required(login_url='login')
def logout_User(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):  # отрисовка главной страницы

    # get_user_vm = VirtMashID.objects.filter(account=request.user)

    usersvm = {}
    get_user_vm = ResourcesProxmox.objects.filter(account=request.user)
    # print(get_user_vm.values_list())
    for user_vm in get_user_vm.values_list():
        name = user_vm[12]
        status = user_vm[16]
        ut = user_vm[18]
        if str(ut) == 'None':
            uptime= 0
        else:
            min = int((ut % 3600) / 60);
            hour = int((ut % 86400) / 3600);
            day = int((ut % 2592000) / 86400);
            uptime = f'{day} дней {hour}:{min}'
        node = user_vm[13]
        uuid = user_vm[0]
        usersvm[user_vm[27]] = name, status, uptime, node, uuid

    context = {'get_all_vm': usersvm}
    if (request.POST):
        login_data = request.POST.dict()
        if 'stop' in login_data:
            uuid = request.POST['Numd']
            instance = ResourcesProxmox.objects.get(uuid=uuid)
            vmStop(proxmoxer_api(), instance.node, instance.vmid)
            return render(request, 'myapp/index.html', context)

        elif 'run' in login_data:
            uuid = request.POST['Numd']
            instance = ResourcesProxmox.objects.get(uuid=uuid)
            vmStart(proxmoxer_api(), instance.node, instance.vmid)
            return render(request, 'myapp/index.html', context)

        elif 'delete' in login_data:
            uuid = request.POST['Numd']
            instance = ResourcesProxmox.objects.get(uuid=uuid)
            deleteVm(proxmoxer_api(), instance.node, instance.vmid)
            instance.delete()
            return render(request, 'myapp/index.html', context)

        elif 'console' in login_data:
            uuid = request.POST['Numd']
            instance = ResourcesProxmox.objects.get(uuid=uuid)
            vnclink = consoleLink(proxmoxer_api(), instance.node, instance.vmid)
            return redirect(vnclink)
            # class ="btn btn-info" onclick="window.open(this.href, 'mywin', 'left=20,top=20,width=700,height=500,toolbar=0,resizable=1'); return false;" > console < / a > -->

    all_vm = resources_get(proxmoxer_api(), 'vm')
    for item in all_vm:
        blog = ResourcesProxmox.objects.get(vmid=item['vmid'])

        for key, value in item.items():
            setattr(blog, key, value)
        blog.save()

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
                     form.cleaned_data['maxcpu'])
            newvm = form.save(commit=False)
            newvm.account = request.user
            newvm.vmid = vmid
            newvm = form.save()

            return redirect(index)
        else:
            form = CreatevmForm()

    return render(request, 'myapp/get_createvm.html', context)


def get_createvm_tm(request):
    form = CreatevmForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CreatevmForm(request.POST)
        if form.is_valid():
            vmid = nextWMID()

            createVM(form.cleaned_data['name'], vmid=vmid)

            newvm_to_base = VirtMashID.objects.create(vmid=vmid, account=request.user)
            newvm_to_base.save()

        # destroyStoppedVM()
        return HttpResponseRedirect('/profile')
    else:
        form = CreatevmForm()
    messages.info(request, 'Your password has been changed successfully!')
    return render(request, 'myapp/get_createvm_tm.html', context)

#
# def vnc(request):
#     all_item = User_list.objects.get()
#     # body = get_console_vnc(all_item.name, all_item.password)
#     context = {'all_item': all_item, }
#
#     return render(request, 'myapp/vnc.html', context)
