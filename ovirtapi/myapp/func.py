import random
import time
import requests
import json

from . import config

from proxmoxer import ProxmoxAPI
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render


def proxmoxer_api():

    #     # if not request.user.is_authenticated():
    #     #     return redirect('/Login?next=%s' % request.path)
    #
    proxmoxIpAddress = config.PROXMOX_SERVER_IP_ADDRESS
    proxmoxUsername = config.PROXMOX_USER
    proxmoxPassword = config.PROXMOX_PASSWORD
    proxmoxVerifySsl = config.PROXMOX_VERIFY_SSL
    #
    proxmox = ProxmoxAPI(proxmoxIpAddress, user=proxmoxUsername, password=proxmoxPassword,
                         verify_ssl=proxmoxVerifySsl)

    return proxmox

    # if not request.user.is_authenticated():
    #     return redirect('/Login?next=%s' % request.path)





def resources_get(proxmox, type):
    return proxmox.cluster.resources.get(type=type)


def nodeList(proxmox):
    nodes_list = [node['node'] for node in proxmox.get('nodes')]
    return nodes_list


def nextWMID(proxmox):
    empty_vmid = proxmox.get('cluster/nextid')
    return empty_vmid


def createVM(proxmox, name, vmid):
    random_node = random.choice(nodeList())
    vmList = [('vmid', vmid),
              ('name', name),
              ('scsi0', 'lvm-shared:20'),
              ('memory', 512),
              ('sockets', 1),
              ('cores', 1),
              ('cpu', 'host'),
              ('net0', 'virtio,bridge=vmbr1'),
              ('cdrom', 'local:iso/debian-11.2.0-amd64-netinst.iso')
              ]

    vm = dict(vmList)
    text = proxmox('nodes')(random_node)('qemu').create(**vm)
    proxmox('cluster')('ha')('resources').create(sid=vm['vmid'])
    return text


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
