
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
    get_user_vm = VirtMashID.objects.filter(account=request.user)
    all_vm = resources_get(proxmoxer_api(), 'vm')
    usersvm = {}
    for vm in all_vm:
        for user_vm in get_user_vm:
            if vm['vmid'] == user_vm.vmid:
                name = vm['name']
                status = vm['status']
                ut = vm['uptime']
                sec = timedelta(seconds=int(ut))
                uptime = (datetime(1, 1, 1) + sec).strftime("%-d days, %H:%M:%S")
                node = vm['node']
                # vnclink

                usersvm[vm['vmid']] = name, status, uptime, node

    if (request.POST):
        login_data = request.POST.dict()

        if 'stop' in login_data:
            vmid = request.POST['Numd']
            for x in resources_get('vm'):
                if x['vmid'] == int(vmid):
                    vmStop(x['node'], vmid)
                    return redirect('index')

    context = {'get_all_vm': usersvm}

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
    # for x in all_vm:
    # print(x)

    # for item_vm in all_vm:
    #     if int(item_vm['vmid']) == int(x):
    #         print(item_vm['vmid'])
    #     print(x)
    # print(type(get_user_vm))

    result_vm = {}
    # for item_vm in all_vm:
    #     if item_vm['vmid'] in get_user_vm:
    #         print(item_vm)

    # nodes_list = [node['node'] for node in proxmox.get('nodes')]

    # for item in get_all_vm:
    #     print(nodes_list)
    # all_item = User_list.objects.get()
    # body = get_vms_login(all_item.name, all_item.password)

    # manage_vm(login_data['up'], 'start', all_item.name, all_item.password)
    #     elif "down" in login_data:
    #         manage_vm(login_data['down'], 'stop', all_item.name, all_item.password)
    #     elif "delete" in login_data:
    #         deletevm(login_data['delete'], all_item.name, all_item.password)
    #     elif "console" in login_data:
    #         get_console_vnc(login_data['console'], all_item.name, all_item.password)
    #         return HttpResponseRedirect(reverse('vnc'))
    #
    #         # context = {'all_item': all_item, 'text': text, 'body': body, }
    #         # return render(request, 'myapp/vnc.html', context)
    context = {'text': text, 'get_all_vm': get_user_vm}
    return render(request, 'myapp/profile.html', context)


def get_createvm(request):
    #     all_item = User_list.objects.get()
    #     body = get_vms_login(all_tem.name, all_item.password)
    form = CreatevmForm()
    context = {'form': form}
    #
    if request.method == 'POST':
        form = CreatevmForm(request.POST)
        if form.is_valid():
            vmid = nextWMID()
            # print(vmid)
            createVM(form.cleaned_data['name'], vmid=vmid)
            newvm_to_base = VirtMashID.objects.create(vmid=vmid, account=request.user)
            newvm_to_base.save()
            # destroyStoppedVM()
            return HttpResponseRedirect('/index')
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
            print(vmid)
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
