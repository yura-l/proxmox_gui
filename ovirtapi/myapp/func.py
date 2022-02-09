import random
import time

import requests
import json
import uuid
from proxmoxer import ProxmoxAPI
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render


def proxmoxer_api():
    proxmox = ProxmoxAPI('aniks-proxmox.o0007.ru:443', user='root@pam',
                         password='1412Flvby', verify_ssl=False)
    return proxmox



def resources_get(type):
    proxmox = proxmoxer_api()
    return proxmox.cluster.resources.get(type=type)

def nodeList():
    proxmox = proxmoxer_api()
    nodes_list = [node['node'] for node in proxmox.get('nodes')]
    return nodes_list


def nextWMID():
    proxmox = proxmoxer_api()
    empty_vmid = proxmox.get('cluster/nextid')
    return empty_vmid


def createVM(name, vmid):
    proxmox = proxmoxer_api()
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

def vmStop(node,vmid):
    proxmox = proxmoxer_api()
    proxmox.create('nodes/%s/qemu/%s/status/stop' %(node, vmid))
    return

def vmStart(node,vmid):
    proxmox = proxmoxer_api()
    proxmox.create('nodes/%s/qemu/%s/status/start' %(node, vmid))
    return


def getNodefromVmid(vmid):
    proxmox = proxmoxer_api()
    for node in nodeList():
        for vm in proxmox.get('nodes/%s/qemu/' % node['node']):
            if vm['status'] == "stopped":
                proxmox.delete('nodes/%s/qemu/%s?destroy-unreferenced-disks=1&purge=1' % (node['node'], vm['vmid']))

