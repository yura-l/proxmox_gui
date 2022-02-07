import random
import time

import requests
import json
import bs4
import uuid
from proxmoxer import ProxmoxAPI
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from myapp.models import VirtMashID


def proxmoxer_api():
    proxmox = ProxmoxAPI('aniks-proxmox.o0007.ru:443', user='root@pam',
                         password='1412Flvby', verify_ssl=False)
    return proxmox


def resources_get(type):
    proxmox = proxmoxer_api()
    return proxmox.cluster.resources.get(type=type)




proxmox = proxmoxer_api()
#
# get_user_vm = VirtMashID.objects.filter(account='user1')
# print(get_user_vm)
# all_vm = resources_get('vm')
# print(all_vm['vmid'])
# x = [102, 101]
# y = resources_get('vm')
#
# for vm in y:
#
#     if vm['vmid'] in x:
#         print(vm[])

# print (x)
# print (y)



    #
    # prox.nodes(<node_name>).lxc.get()
    # prox.nodes(<node_name>).get('lxc')
    # prox.get('nodes/%s/lxc' % <node_name>)
    # prox.get('nodes', <node_name>, 'lxc')
    # prox('nodes')(<node_name>).lxc.get()
    # prox(['nodes', <node_name>]).lxc.get()
    # prox(['nodes', <node_name>]).get('lxc')
    # prox('nodes')(<node_name>)('lxc').get()
