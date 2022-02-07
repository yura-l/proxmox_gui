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






#
#
# def disk_create_no_template(vm_name, hdd_size, namedisk):
#     text = f"""
#         <disk_attachment>
#             <bootable>true</bootable>
#             <interface>virtio</interface>
#             <active>true</active>
#             <disk>
#                 <description>disk{vm_name}</description>
#                 <format>cow</format>
#                 <name>{namedisk}</name>
#                 <provisioned_size>{hdd_size}</provisioned_size>
#                 <storage_domains>
#                     <storage_domain id="0b27fe8c-cbe3-4657-bfe9-4083ab6aab3b"/>
#                 </storage_domains>
#             </disk>
#         </disk_attachment>"""
#     return text
#
#
# def disk_resize(hdd_size):
#     text = f"""
#           <disk>
#         <provisioned_size>{hdd_size}</provisioned_size>
#     </disk>"""
#     return text
#
#
# def lan_create():
#     text = f"""
#         <nic>
#             <name>lan</name>
#             <interface>virtio</interface>
#             <vnic_profile href="/ovirt-engine/api/vnicprofiles/2ecfee9d-632c-433f-8de3-c848bb64b4bf" id="2ecfee9d-632c-433f-8de3-c848bb64b4bf" />
#         </nic>"""
#     return text
#
#
# def get_key(username, password):
#     response = requests.get(
#         'https://ovirt2-engine.test.local/ovirt-engine/sso/oauth/token', verify=False,
#         params={'grant_type': 'password',
#                 'scope': 'ovirt-app-api',
#                 'username': username,
#                 'password': password},
#         headers={'Accept': 'application/json',
#                  'Content-Type': 'application/x-www-form-urlencoded'})
#     key = json.loads(response.text)
#     return (key['access_token'])
#
#
# # def get_datacenter():
# #     response = requests.get(
# #         'https://ovirt2-engine.test.local/ovirt-engine/api/datacenters', verify=False,
# #
# #         headers={'Accept': 'application/xml',
# #
# #                  'Authorization': 'Bearer ' + get_key('', '')},
# #     )
# #     if response.status_code == 200:
# #         soup = bs4.BeautifulSoup(response.text, 'lxml')
# #         dc_list = [x.get_text(strip=True) for x in soup.select('name')]
# #         return dc_list
#
#
# # def get_vms():
# #     response = requests.get(
# #         'https://ovirt2-engine.test.local/ovirt-engine/api/vms', verify=False,
# #
# #         headers={'Accept': 'application/xml',
# #                  'Authorization': 'Bearer ' + get_key('admin@internal', '')},
# #     )
# #     if response.status_code == 200:
# #         soup = bs4.BeautifulSoup(response.text, 'lxml')
# #         x = soup.findAll("vm")
# #         vm_name = {}
# #         for item in x:
# #             z = item.find('name').text
# #             r = item.get('id')
# #             status = item.find('status').text
# #             url_stop = item.find("link", {"rel": "stop"})['href']
# #             # print(the_url)
# #             vm_name[z] = r, status, url_stop
# #
# #         return vm_name
#
#
# def manage_vm(vmid, run, username, password):
#     data = """<action/>"""
#     response = requests.post(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/vms/' + vmid + '/' + run, data=data, verify=False,
#
#         headers={'Accept': 'application/xml',
#                  'Content-Type': 'application/xml',
#                  'Authorization': 'Bearer ' + get_key(username, password)},
#     )
#     if response.status_code == 200:
#         return
#
#
# def get_vms_login(username, password):
#     response = requests.get(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/vms', verify=False,
#
#         headers={'Accept': 'application/xml',
#                  'Authorization': 'Bearer ' + get_key(username, password)},
#     )
#     if response.status_code == 200:
#         soup = bs4.BeautifulSoup(response.text, 'lxml')
#         all_vms_user = soup.findAll("vm")
#         vm_info = {}
#         for vm in all_vms_user:
#             vm_comment = vm.find('comment').text
#             vm_id = vm.get('id')
#             vm_status = vm.find('status').text
#             vm_url_stop = vm.find("link", {"rel": "stop"})['href']
#             # print(url_stop)
#             vm_info[vm_id] = vm_comment, vm_status, vm_url_stop
#
#         # print(vm_info)
#         return vm_info
#
#
# # def create_user_ovirt(username,password):
# #     host = 'ovirt2-engine.test.local '
# #     user = username
# #     secret = password
# #     port = 22
# #
# #     client = paramiko.SSHClient()
# #     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# #     client.connect(hostname=host, username=user, password=secret, port=port)
# #     stdin, stdout, stderr = client.exec_command('ls -l')
# #     data = stdout.read() + stderr.read()
# #     client.close()
# #     return print(data)
#
#
# # def index(request):
# #     if (request.POST):
# #         login_data = request.POST.dict()
# #         if 'up' in login_data:
# #             manage_vm(login_data['up'], 'start')
# #         elif "down" in login_data:
# #             manage_vm(login_data['down'], 'stop')
# #
# #     return render(request, 'myapp/index.html', {'body': get_vms})
# def deletevm(vm_name, username, passwd):
#     response = requests.delete(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/vms/' + vm_name, verify=False,
#
#         headers={'Accept': 'application/xml',
#                  'Content-Type': 'application/xml',
#                  'Authorization': 'Bearer ' + get_key(username, passwd)},
#     )
#
#
# def create_vm(username, passwd, vm_name, cpu, mem, hdd, template, vm_hostname, vm_username, vm_password):
#     data = f"""
#             <vm>
#             <name>{uuid.uuid4()}</name>
#             <comment>{vm_name}</comment>
#             <cluster>
#                 <name>cl1</name>
#             </cluster>
#             <template>
#                 <name>{template}</name>
#             </template>
#             <memory>{mem}</memory>
#     		<memory_policy>
#     		    <ballooning>true</ballooning>
#     		    <guaranteed>536870912</guaranteed>
#     		    <max>{mem}</max>
#     		</memory_policy>
#             <os>
#                 <boot dev="hd"/>
#             </os>
#             <cpu_profile id="02eb3942-9669-440c-a282-72fee895776d"/>
#             	<initialization>
#                      <cloud_init>
#                   <host>
#                      <address>{vm_hostname}</address>
#                   </host>
#                      <users>
#                         <user>
#                             <user_name>{vm_username}</user_name>
#                             <password>{vm_password}</password>
#                          </user>
#                       </users>
# 	         </cloud_init>
#         </initialization>
#     	</vm>
#         """
#     # print(data)
#     # print(data2)
#     beaver_key = get_key(username, passwd)
#     response = requests.post(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/vms', verify=False,
#
#         headers={'Accept': 'application/xml',
#                  'Content-Type': 'application/xml',
#                  'Authorization': 'Bearer ' + beaver_key},
#         data=data,
#
#     )
#     if response.status_code == 201 or response.status_code == 202:
#         soup = bs4.BeautifulSoup(response.text, 'lxml')
#         # print(soup)
#         # print('-'*100)
#         all_vms_user = soup.findAll("vm")
#         # print(all_vms_user)
#         vm_id = ''
#         for vm in all_vms_user:
#             # vm_comment = vm.find('comment').text
#             vm_id = vm.get('id')
#             # print(vm_id)
#         #     vm_status = vm.find('status').text
#         #     vm_url_stop = vm.find("link", {"rel": "stop"})['href']
#         #     # print(url_stop)
#         #     vm_info[vm_id] = vm_comment, vm_status, vm_url_stop
#         response_hdd = requests.get(
#             'https://ovirt2-engine.test.local/ovirt-engine/api/vms/' + vm_id + '/diskattachments', verify=False,
#
#             headers={'Accept': 'application/xml',
#                      'Authorization': 'Bearer ' + beaver_key},
#         )
#         if response_hdd.status_code == 200:
#             soup = bs4.BeautifulSoup(response_hdd.text, 'lxml')
#             disk_attachment = soup.findAll("disk_attachment")
#             disk_id = ''
#             for disk in disk_attachment:
#                 # vm_comment = vm.find('comment').text
#                 disk_id = disk.get('id')
#
#             data_disk_size = disk_resize(hdd)
#
#             datalan = lan_create()
#             responselan = requests.post(
#                 'https://ovirt2-engine.test.local/ovirt-engine/api/vms/' + vm_id + '/nics', verify=False,
#
#                 headers={'Accept': 'application/xml',
#                          'Content-Type': 'application/xml',
#                          'Authorization': 'Bearer ' + beaver_key},
#                 data=datalan,
#             )
#             # time.sleep(20)
#             x = 0
#             response_resize = requests.put(
#                 'https://ovirt2-engine.test.local/ovirt-engine/api/disks/' + disk_id, verify=False,
#
#                 headers={'Accept': 'application/xml',
#                          'Content-Type': 'application/xml',
#                          'Authorization': 'Bearer ' + beaver_key},
#                 data=data_disk_size,
#             )
#             while response_resize.status_code == 409:
#                 response_resize = requests.put(
#                     'https://ovirt2-engine.test.local/ovirt-engine/api/disks/' + disk_id, verify=False,
#
#                     headers={'Accept': 'application/xml',
#                              'Content-Type': 'application/xml',
#                              'Authorization': 'Bearer ' + beaver_key},
#                     data=data_disk_size,
#                 )
#                 x = x + 1
#                 print(x)
#
#         return
#
#
# def get_console_vnc(vm_id, username, passwd):
#     responsevnc = requests.get(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/vms/' + vm_id + '/graphicsconsoles', verify=False,
#
#         headers={'Accept': 'application/xml',
#                  'Content-Type': 'application/xml',
#                  'Authorization': 'Bearer ' + get_key(username, passwd)},
#
#     )
#     if responsevnc.status_code == 200:
#         soup = bs4.BeautifulSoup(responsevnc.text, 'lxml')
#         vnc = soup.findAll('link')
#         for item in vnc:
#             x = item.get('href')
#             x = x.split("/")
#
#     remote_viewer_connection_file = requests.post(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/vms/8f6ff648-eed4-44d7-9986-968c783424f5/graphicsconsoles/' +
#         x[6] + '/remoteviewerconnectionfile', verify=False,
#
#         headers={'Accept': 'application/xml',
#                  'Content-Type': 'application/xml',
#                  'Authorization': 'Bearer ' + get_key(username, passwd)},
#         data="<action/>",
#     )
#     print(remote_viewer_connection_file.status_code)
#     print(remote_viewer_connection_file.text)
#
#     proxyticket = requests.post(
#         'https://ovirt2-engine.test.local/ovirt-engine/api/vms/8f6ff648-eed4-44d7-9986-968c783424f5/graphicsconsoles/' +
#         x[6] + '/proxyticket', verify=False,
#
#         headers={'Accept': 'application/xml',
#                  'Content-Type': 'application/xml',
#                  'Authorization': 'Bearer ' + get_key(username, passwd)},
#         data="<action/>",
#     )
#     print(proxyticket.status_code)
#     print(proxyticket.text)
#
#
#
#     # print (responsevnc.status_code)
#     # print (vnc)
#     # print('-----'*40)
#     # print(soup.prettify())
#     # return  HttpResponseRedirect('/vnc')
#
#
# def create_disk(*args):
#     return print(*args)
#
#
# def connect_lan(*args):
#     return
#
# #
# # def get_userid(request, pk):
# #     userlist = User_list.objects.get(id=pk)
# #     listusers = {}
# #
# #
# #     body = get_vms_login(userlist.name, userlist.password)
# #     context = {'userlist': userlist, 'body': body}
# #     return render(request, 'myapp/profile.html', context)
# #
# #
# # def get_createvm(request, pk):
# #     userlist = User_list.objects.get(id=pk)
# #     body = get_vms_login(userlist.name, userlist.password)
# #     form = CreatevmForm()
# #     context = {'userlist': userlist, 'body': body, 'form': form}
# #
# #     if request.method == 'POST':
# #         form = CreatevmForm(request.POST)
# #         if form.is_valid():
# #             # prin/t(frm.cleaned_data)
# #             create_vm(userlist.name, userlist.password, form.cleaned_data['name'], form.cleaned_data['cpu'],
# #                       form.cleaned_data['mem'], form.cleaned_data['hdd'], form.cleaned_data['template'])
# #             return HttpResponseRedirect("/users%i" % (int(pk)))
# #         else:
# #             form = CreatevmForm()
# #
# #     return render(request, 'myapp/get_createvm.html', context)
# #
# #
# # def get_console(request):
# #     if (request.GET.get('mybtn')):
# #         print(request.GET)
# #         return render(request, 'myapp/get_console.html')
# #
# #
# # def delete_vm(request, pk, vm):
# #     userlist = User_list.objects.get(id=pk)
# #     listusers = {}
# #     pk = pk
# #     vm = vm
# #     if (request.POST):
# #         data = request.POST.dict()
# #         # print(data)
# #         if 'vm' in data:
# #             deletevm(data['vm'], pk, userlist.name, userlist.password)
# #             return HttpResponseRedirect("/users%i" % (int(pk)))
# #
# #     # body = get_vms_login(userlist.name, userlist.password)
# #     context = {'userlist': userlist, 'vm': vm, 'pk': pk, }
# #
# #     return render(request, 'myapp/delete.html', context)
