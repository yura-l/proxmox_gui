import os
import random
import time
import requests
import json

from . import config

from proxmoxer import ProxmoxAPI
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render

from .models import ResourcesProxmox
from django.conf import settings


def proxmoxer_api():
    proxmoxIpAddress = config.PROXMOX_SERVER_IP_ADDRESS
    proxmoxUsername = config.PROXMOX_USER

    proxmoxVerifySsl = config.PROXMOX_VERIFY_SSL
    proxmoxtValue = config.TOKEN_VALUE
    proxmoxtName = config.TOKEN_NAME
    proxmox = ProxmoxAPI(proxmoxIpAddress, user=proxmoxUsername, token_name=proxmoxtName,
                         token_value=proxmoxtValue, verify_ssl=proxmoxVerifySsl)

    return proxmox

    # if not request.user.is_authenticated():
    #     return redirect('/Login?next=%s' % request.path)


def resources_get(proxmox, type):
    return proxmox.cluster.resources.get(type=type)


def UpdateBase(data_dict):
    m = ResourcesProxmox(**data_dict)
    # don't forget to save to database!
    m.save()

def nodeList(proxmox):
    nodes_list = [node['node'] for node in proxmox.get('nodes')]
    return nodes_list


def nextWMID(proxmox):
    empty_vmid = proxmox.get('cluster/nextid')
    return empty_vmid


def check_status(proxmox, node, upid):
    task = proxmox.get('nodes/%s/tasks/%s/status' % (node, upid))
    return task


def createVM(proxmox, name, vmid, maxmem, maxdisk, maxcpu, cdrom):
    random_node = random.choice(nodeList(proxmox))
    vmList = [('vmid', vmid),
              ('name', name),
              ('scsi0', f'lvm-shared:{maxdisk}'),
              ('memory', maxmem),
              ('sockets', 1),
              ('cores', maxcpu),
              ('cpu', 'host'),
              ('net0', 'virtio,bridge=vmbr1'),
              ('cdrom', cdrom)
              ]

    vm = dict(vmList)

    x = proxmox('nodes')(random_node)('qemu').create(**vm)
    y = check_status(proxmox, random_node, x)
    while y['status'] != "stopped":
        y = check_status(proxmox, random_node, x)

    y = check_status(proxmox, random_node, x)
    if y['exitstatus'] != "OK":
        return "ERROR"
    else:
        # print(y)
        stat = proxmox.get('nodes/%s/qemu/%s/status/current' % (random_node, y['id']))
        # print(stat)
        proxmox('cluster')('ha')('resources').create(sid=vm['vmid'])
        return



def access_ticket():
    proxmoxIpAddress = config.PROXMOX_SERVER_IP_ADDRESS
    proxmoxUsername = config.PROXMOX_USER
    proxmoxVerifySsl = config.PROXMOX_VERIFY_SSL
    proxmoxtPassword = config.PROXMOX_PASSWORD
    proxmox = ProxmoxAPI(proxmoxIpAddress, user=proxmoxUsername,
                         password=proxmoxtPassword, verify_ssl=proxmoxVerifySsl)
    # username = 'root@pam'
    # password = '1412Flvby'

    username = 'user_console@pve'
    password = 'user_console'

    return proxmox.access.ticket.create(username=username, password=password)





# def createVM(name, vmid):
#     proxmox = proxmoxer_api()
#     random_node = random.choice(nodeList())
#     vmList = [('vmid', vmid),
#                ('name', name),
#                ('scsi0', 'lvm-shared:20'),
#                ('memory', 512),
#                ('sockets', 1),
#                ('cores', 1),
#                ('cpu', 'host'),
#                ('net0', 'virtio,bridge=vmbr1'),
#                ('cdrom', 'local:iso/debian-11.2.0-amd64-netinst.iso')
#                ]
#
#     vm = dict(vmList)
#     text = proxmox('nodes')(random_node)('qemu').create(**vm)
#     proxmox('cluster')('ha')('resources').create(sid=vm['vmid'])
#     return text
#
# create /nodes/{node}/qemu/{vmid}/clone

def deleteVm(proxmox, node, vmid):
    proxmox.delete('nodes/%s/qemu/%s?destroy-unreferenced-disks=1&purge=1' % (node, vmid))


def destroyStoppedVM():
    proxmox = proxmoxer_api()
    for node in proxmox.get('nodes'):
        for vm in proxmox.get('nodes/%s/qemu/' % node['node']):
            if vm['status'] == "stopped":
                proxmox.delete('nodes/%s/qemu/%s?destroy-unreferenced-disks=1&purge=1' % (node['node'], vm['vmid']))


def vmStop(proxmox, node, vmid):
    proxmox.create('nodes/%s/qemu/%s/status/stop' % (node, vmid))
    return HttpResponse("Ok")


def vmStart(proxmox, node, vmid):
    proxmox.create('nodes/%s/qemu/%s/status/start' % (node, vmid))
    return HttpResponse("Ok")


def getNodefromVmid(vmid):
    proxmox = proxmoxer_api()
    for node in nodeList():
        for vm in proxmox.get('nodes/%s/qemu/' % node['node']):
            if vm['status'] == "stopped":
                proxmox.delete('nodes/%s/qemu/%s?destroy-unreferenced-disks=1&purge=1' % (node['node'], vm['vmid']))


def consoleLink(proxmox, node, vmid):
    configvnc = proxmox.create("nodes", node, "qemu", vmid, 'vncproxy?websocket=1')
    vnclink = (f"https://aniks-proxmox.o0007.ru/?console=kvm&novnc=1&node=%s&resize=scale&vmid=%s&path=api2/json/nodes/%s/qemu/%s/vncwebsocket?port=443&vncticket={configvnc['ticket']}" %(
    node, vmid, node, vmid))
    return vnclink


def storage_item_iso(proxmox):
    stor_iso = {'':'Выбрать образ ОС'}
    list_iso = proxmox.nodes('pve-223').storage.local.content.get()
    for i in list_iso:
        if i['volid'].endswith('.iso'):
            stor_iso[(i['volid'])] = i['volid'].split('/')[1]
    return stor_iso


def graf_png(type, node, vmid, uuid):
    proxmox = proxmoxer_api()
    response = proxmox.nodes(node).qemu(vmid).rrd.get(ds=type, timeframe='day')
    # proxmox.get("nodes", node, "qemu", vmid, "rrd", f'?ds={type},timeframe={period})
    full_filename = os.path.join(settings.MEDIA_ROOT, uuid)
    try:
        os.mkdir(full_filename)
    except:
        pass

    with open(f'{full_filename}\{type}.png', 'wb') as f:
        f.write(response['image'].encode('raw_unicode_escape'))
    return