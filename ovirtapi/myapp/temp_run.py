import os
import random
import time

import requests
import json

from django.conf import settings
from proxmoxer import ProxmoxAPI
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render

#
#
from ovirtapi.myapp import config

from proxmoxer import ProxmoxAPI


def proxmoxer_api():
    #     # if not request.user.is_authenticated():
    #     #     return redirect('/Login?next=%s' % request.path)
    #
    proxmoxIpAddress = config.PROXMOX_SERVER_IP_ADDRESS
    proxmoxUsername = config.PROXMOX_USER
    proxmoxVerifySsl = config.PROXMOX_VERIFY_SSL
    proxmoxtValue = config.TOKEN_VALUE
    proxmoxtName = config.TOKEN_NAME
    proxmox = ProxmoxAPI(proxmoxIpAddress, user=proxmoxUsername, token_name=proxmoxtName,
                         token_value=proxmoxtValue, verify_ssl=proxmoxVerifySsl)

    return proxmox


def resources_get(proxmox, type):
    return proxmox.cluster.resources.get(type=type)


def destroyStoppedVM():
    proxmox = proxmoxer_api()
    y = ()
    for node in proxmox.get('nodes'):
        for vm in proxmox.get('nodes/%s/qemu/' % node['node']):
            if vm['status'] == "stopped":
                proxmox.delete('nodes/%s/qemu/%s?destroy-unreferenced-disks=1&purge=1' % (node['node'], vm['vmid']))

    return


def access_ticket():
    proxmoxIpAddress = config.PROXMOX_SERVER_IP_ADDRESS
    proxmoxUsername = config.PROXMOX_USER
    proxmoxVerifySsl = config.PROXMOX_VERIFY_SSL
    proxmoxtPassword = config.PROXMOX_PASSWORD
    proxmox = ProxmoxAPI(proxmoxIpAddress, user=proxmoxUsername,
                         password=proxmoxtPassword, verify_ssl=proxmoxVerifySsl)
    username = 'user_console@pve'
    password = 'user_console'

    return proxmox.access.ticket.create(username=username, password=password)




def basic_blocking_task_status(proxmox_api, task_id, node_name):
    data = {"status": ""}
    while (data["status"] != "stopped"):
        data = proxmox_api.nodes(node_name).tasks(task_id).status.get()

    return data




def graf_png(type):
    proxmox = proxmoxer_api()
    response = proxmox.nodes('pve-225').rrd.get(ds=type, timeframe='day')
    full_filename = os.path.join(settings.STATIC_ROOT)
    print(full_filename)
    with open(f'{type}.png', 'wb') as f:
        f.write(response['image'].encode('raw_unicode_escape'))
    return f


graf_png('cpu')

#
#
# def createVM(proxmox, name, vmid):
#     random_node = random.choice(nodeList(proxmox))
#     vmList = [('vmid', vmid),
#               ('name', name),
#               ('scsi0', 'lvm-shared:20'),
#               ('memory', 512),
#               ('sockets', 1),
#               ('cores', 1),
#               ('cpu', 'host'),
#               ('net0', 'virtio,bridge=vmbr1'),
#               ('cdrom', 'local:iso/debian-11.2.0-amd64-netinst.iso')
#               ]
#
#     vm = dict(vmList)
#     text = proxmox('nodes')(random_node)('qemu').create(**vm)
#     proxmox('cluster')('ha')('resources').create(sid=vm['vmid'])
#     return proxmox
#
#
#

#     # command = request.GET.get('command', 'none')
#     # currentNode = request.GET.get('node', 'none')
#     # currentVz = request.GET.get('openvz', 'none')
#     # currentVm = request.GET.get('qemu', 'none')
#     #
#     # if command != 'none':
#     #     return runcommand(request, proxmox)
#     # elif currentVz != 'none':
#     #     vms = getVmDict(proxmox)
#     #     tasks = getAllServerTasks(proxmox)
#     #     return render(request, 'OctaHomeProxmox/CT.html',
#     #                   {'links': getSideBar(request, proxmox), 'serverInfo': addWizardVeriables(request, proxmox),
#     #                    'node': currentNode, 'Vz': vms[currentNode][currentVz],
#     #                    'StorageDevices': getStorageDetails(proxmox), 'ServerStatuses': getServerStatuses(proxmox),
#     #                    'tasks': tasks})
#     # elif currentVm != 'none':
#     #     raise Http404
#     # elif currentNode != 'none':
#     #     tasks = proxmox.nodes(currentNode).get('tasks')
#     #     return render(request, 'OctaHomeProxmox/Node.html',
#     #                   {'links': getSideBar(request, proxmox), 'serverInfo': addWizardVeriables(request, proxmox),
#     #                    'Node': currentNode, 'StorageDevices': getStorageDetails(proxmox),
#     #                    'ServerStatuses': getServerStatuses(proxmox), 'tasks': tasks})
#     # else:
#     #     tasks = getAllServerTasks(proxmox)
#     #     return render(request, 'OctaHomeProxmox/AllNodes.html',
#     #                   {'links': getSideBar(request, proxmox), 'serverInfo': addWizardVeriables(request, proxmox),
#     #                    'StorageDevices': getStorageDetails(proxmox), 'ServerStatuses': getServerStatuses(proxmox),
#     #                    'tasks': tasks})
#     # raise Http404
#
# #
# # def resources_get(type):
# #     proxmox = proxmoxer_api()
# #     return proxmox.cluster.resources.get(type=type)
#
#
# def getVmDict(proxmox):
#     nodes = {}
#
#     for anode in proxmox.nodes.get():
#         vms = {}
#         for avm in proxmox.nodes(anode['node']).openvz.get():
#             vms[str(avm['vmid'])] = avm
#
#         for avm in proxmox.nodes(anode['node']).qemu.get():
#             vms[str(avm['vmid'])] = avm
#
#         nodes[str(anode['node'])] = vms
#
#     return nodes
#
# print(getVmDict(ProxmoxMain()))
#
# def addWizardVeriables(request, proxmox):
#     nodes = []
#     templates = []
#     csrftoken = get_token(request)
#
#     for node in proxmox.nodes.get():
#         nodes.append(node['node'])
#
#     for node in proxmox.nodes.get():
#         nodeTemplates = []
#         for item in proxmox.nodes(node['node']).storage.local.content.get():
#             if item['content'] == 'vztmpl':
#                 nodeTemplates.append(item['volid'])
#         templates.append({'node': node['node'], 'templates': nodeTemplates})
#
#     return {'nodes': nodes, 'templates': templates, 'csrftoken': csrftoken}
#
#
# def getSideBar(request, proxmox):
#     currentPage = request.GET.get('currentPage', 'all')
#     currentNode = request.GET.get('node', 'none')
#     currentVz = request.GET.get('openvz', 'none')
#     currentCt = request.GET.get('qemu', 'none')
#
#     links = [{'title': 'System Stats', 'address': '/Proxmox/',
#               'active': getSideBarActiveState([currentNode, currentVz, currentCt], 'none')}]
#
#     for node in proxmox.nodes.get():
#         nodeSublinks = []
#         containers = []
#         for vm in proxmox.nodes(node['node']).openvz.get():
#             sidebarItem = {'title': vm['vmid'] + ": " + vm['name'],
#                            'address': '/Proxmox/?node=' + node['node'] + '&openvz=' + vm['vmid'],
#                            'active': getSideBarActiveState(vm['vmid'], currentVz)}
#             containers.append(sidebarItem)
#         sidebarItem = {'title': 'CT\'s', 'sublinks': containers, 'active': ''}
#         nodeSublinks.append(sidebarItem)
#
#         vms = []
#         for vm in proxmox.nodes(node['node']).qemu.get():
#             sidebarItem = {'title': vm['vmid'] + ": " + vm['name'],
#                            'address': '/Proxmox/?node=' + node['node'] + '&qemu=' + vm['vmid'],
#                            'active': getSideBarActiveState(vm['vmid'], currentCt)}
#             vms.append(sidebarItem)
#         sidebarItem = {'title': 'VM\'s', 'sublinks': vms, 'active': ''}
#         nodeSublinks.append(sidebarItem)
#
#         nodeItem = {'title': node['node'], 'address': '/Proxmox/?node=' + node['node'], 'sublinks': nodeSublinks,
#                     'active': getSideBarActiveState(node['node'], currentNode)}
#         links.append(nodeItem)
#
#     sidebarItem = {'title': 'Add New Server', 'address': '', 'id': 'addServer',
#                    'active': getSideBarActiveState('add', currentPage)}
#     links.append(sidebarItem)
#     return links
#
#
# def getSideBarActiveState(sidebarItem, currentPage):
#     if type(sidebarItem) is list:
#         for anItem in sidebarItem:
#             if anItem != currentPage:
#                 return ''
#         return 'active'
#     if sidebarItem == currentPage:
#         return 'active'
#     else:
#         return ''
#
#
# def getAllServerTasks(proxmox):
#     toReturn = []
#     for node in proxmox.nodes.get():
#         toReturn = toReturn + proxmox.nodes(node['node']).get('tasks')
#     return toReturn
#
#
# def getServerStatuses(proxmox):
#     containersOnline = 0
#     containersTotal = 0
#     vmsOnline = 0
#     vmsTotal = 0
#
#     serverUptimes = []
#
#     for node in proxmox.nodes.get():
#         uptime = datetime.timedelta(seconds=node['uptime'])
#         uptimeItem = {'node': node['node'], 'uptime': uptime, 'secondUptime': node['uptime']}
#         serverUptimes.append(uptimeItem)
#         for vm in proxmox.nodes(node['node']).openvz.get():
#             containersTotal = containersTotal + 1
#             if vm['status'] == "running":
#                 containersOnline = containersOnline + 1
#         for vm in proxmox.nodes(node['node']).qemu.get():
#             vmsTotal = vmsTotal + 1
#             if vm['status'] == "running":
#                 vmsOnline = vmsOnline + 1
#
#     totalOnline = containersOnline + vmsOnline
#     totalTotal = containersTotal + vmsTotal
#
#     totalOnlinePercentage = float(100 * float(float(totalOnline) / float(totalTotal)))
#     totalOffLinePercentage = float(100 * float(float(totalTotal - totalOnline) / totalTotal))
#     result = {}
#
#     result['uptimes'] = serverUptimes
#
#     result['containersOnline'] = str(containersOnline)
#     result['containersTotal'] = str(containersTotal)
#
#     result['vmsOnline'] = str(vmsOnline)
#     result['vmsTotal'] = str(vmsTotal)
#
#     result['totalOnline'] = str(totalOnline)
#     result['totalTotal'] = str(totalTotal)
#
#     result['totalOnlinePercentage'] = str(totalOnlinePercentage)
#     result['totalOffLinePercentage'] = str(totalOffLinePercentage)
#
#     return result
#
#
# def getStorageDetails(proxmox):
#     toReturn = {}
#     numberOfDevices = 0
#     numberOfNodes = 0
#     totalSpace = 0
#     totalSpaceGB = float(0)
#     totalUsed = 0
#     totalUsedGB = float(0)
#     nodeStorageDevices = []
#     allStorageDevice = []
#     for node in proxmox.nodes.get():
#         numberOfNodes = numberOfNodes + 1
#         nodeStorageDevices = proxmox.nodes(node['node']).get('storage')
#
#         nodeNumberOfStorageDevices = 0
#         nodeTotalSpaceGb = float(0)
#         nodeUsedSpaceGb = float(0)
#
#         for nodeStorageDevice in nodeStorageDevices:
#             name = nodeStorageDevice['storage']
#             numberOfDevices = numberOfDevices + 1
#             nodeNumberOfStorageDevices = nodeNumberOfStorageDevices + 1
#
#             totalSpace = totalSpace + int(nodeStorageDevice['total'])
#             totalUsed = totalUsed + int(nodeStorageDevice['used'])
#
#             gbTotalSpace = float(float(nodeStorageDevice['total']) / float(1073741824))
#             gbSpaceUsed = float(float(nodeStorageDevice['used']) / float(1073741824))
#
#             totalSpaceGB = totalSpaceGB + gbTotalSpace
#             totalUsedGB = totalUsedGB + gbSpaceUsed
#
#             nodeTotalSpaceGb = nodeTotalSpaceGb + gbTotalSpace
#             nodeUsedSpaceGb = nodeUsedSpaceGb + gbSpaceUsed
#
#             aDevice = {'node': node['node'], 'name': name, 'total': nodeStorageDevice['total'],
#                        'used': nodeStorageDevice['used'], 'totalGb': totalSpaceGB, 'usedGb': totalUsedGB}
#             allStorageDevice.append(aDevice)
#
#         aNode = {'node': node['node'], 'totalGb': nodeTotalSpaceGb, 'usedGb': nodeUsedSpaceGb}
#         nodeStorageDevices.append(aNode)
#
#     allItem = {'total': totalSpace, 'used': totalUsed, 'nodes': numberOfNodes, 'devices': numberOfDevices,
#                'totalGb': totalSpaceGB, 'usedGb': totalUsedGB}
#     toReturn['all'] = allItem
#     toReturn['devices'] = allStorageDevice
#     toReturn['nodes'] = nodeStorageDevices
#
#     return toReturn
#
#
# # proxmox = proxmoxer_api()
# # y = 104
# # for x in resources_get('vm'):
# #     if y == x['vmid']:
# #         print(x['node'])
#
# #
# # get_user_vm = VirtMashID.objects.filter(account='user1')
# # print(get_user_vm)
# # all_vm = resources_get('vm')
# # print(all_vm['vmid'])
# # x = [102, 101]
# # y = resources_get('vm')
# #
# # for vm in y:
# #
# #     if vm['vmid'] in x:
# #         print(vm[])
#
# # print (x)
# # print (y)
#
#
#
#     #
#     # prox.nodes(<node_name>).lxc.get()
#     # prox.nodes(<node_name>).get('lxc')
#     # prox.get('nodes/%s/lxc' % <node_name>)
#     # prox.get('nodes', <node_name>, 'lxc')
#     # prox('nodes')(<node_name>).lxc.get()
#     # prox(['nodes', <node_name>]).lxc.get()
#     # prox(['nodes', <node_name>]).get('lxc')
#     # prox('nodes')(<node_name>)('lxc').get()
#
#
# def runcommand(request, proxmox):
#     command = request.GET.get('command', 'none')
#     if command == 'startCT':
#         node = str(request.GET.get('node', ''))
#         ct = str(request.GET.get('ct', ''))
#         proxmox.nodes(node).openvz(ct).status.start.post()
#         return HttpResponse("Ok")
#     elif command == 'stopCT':
#         node = str(request.GET.get('node', ''))
#         ct = str(request.GET.get('ct', ''))
#         proxmox.nodes(node).openvz(ct).status.stop.post()
#         return HttpResponse("Ok")
#     elif command == 'shutdownCT':
#         node = str(request.GET.get('node', ''))
#         ct = str(request.GET.get('ct', ''))
#         proxmox.nodes(node).openvz(ct).status.shutdown.post()
#         return HttpResponse("Ok")
#     elif command == 'migrateCT':
#         node = str(request.GET.get('node', ''))
#         ct = str(request.GET.get('ct', ''))
#         target = str(request.GET.get('target', ''))
#         proxmox.nodes(node).openvz(ct).migrate.post(target=target)
#
#         return HttpResponse("Ok")
#     elif command == 'consoleCT':
#         node = str(request.GET.get('node', ''))
#         ct = str(request.GET.get('ct', ''))
#         vnc = proxmox.nodes(node).openvz(ct).vncproxy.post()
#         vnc['cert'] = vnc['cert'].replace('\n', '|')
#         return render(request, 'pages/Proxmox/console.html', {'vnc': vnc})
#     elif command == 'removeCT':
#         node = str(request.GET.get('node', ''))
#         ct = str(request.GET.get('ct', ''))
#         proxmox.nodes(node).openvz(ct).delete()
#         return HttpResponse("Ok")
#     elif command == 'startVM':
#         raise NameError('Yet To Be Implemented')
#     elif command == 'stopVM':
#         raise NameError('Yet To Be Implemented')
#     elif command == 'shutdownVM':
#         raise NameError('Yet To Be Implemented')
#     elif command == 'migrateVM':
#         raise NameError('Yet To Be Implemented')
#     elif command == 'consoleVM':
#         raise NameError('Yet To Be Implemented')
#     elif command == 'removeVM':
#         raise NameError('Yet To Be Implemented')
#     elif command == 'addcomplete':
#         nodeLocation = request.POST.get('node', '')
#         vmid = request.POST.get('vmid', '')
#         template = request.POST.get('template', '')
#         hostname = request.POST.get('hostname', '')
#         storage = request.POST.get('storage', 'local')
#         memory = request.POST.get('memory', '')
#         swap = request.POST.get('swap', '')
#         cpus = request.POST.get('cpu', '')
#         disk = request.POST.get('disk', '')
#         password = request.POST.get('serverpw', '')
#         ipaddress = request.POST.get('ipaddress', '')
#
#         if vmid == '':
#             vmid = 100
#
#             ids = []
#
#             for node in proxmox.nodes.get():
#                 for vm in proxmox.nodes(node['node']).openvz.get():
#                     ids.append(int(vm['vmid']))
#
#                 for vm in proxmox.nodes(node['node']).qemu.get():
#                     ids.append(int(vm['vmid']))
#
#             while (vmid in ids):
#                 vmid = vmid + 1
#
#         node = proxmox.nodes(nodeLocation)
#         if node != None:
#             node.openvz.create(vmid=int(vmid), ostemplate=str(template), hostname=str(hostname), storage=str(storage),
#                                memory=int(memory), swap=int(swap), cpus=int(cpus), disk=int(disk),
#                                password=str(password), ip_address=str(ipaddress))
#         else:
#             return HttpResponse("Node Not Found", status=400)
#
#         return HttpResponse("Ok")
#     elif command == 'nodeStats':
#         node = str(request.GET.get('node', ''))
#         timeFrame = str(request.GET.get('time', 'hour'))
#
#         stats = proxmox.nodes(node).rrddata.get(timeframe=timeFrame)
#
#         text = json.dumps(stats, separators=(',', ':'))
#
#         return HttpResponse(text)
#     elif command == 'ctStats':
#         node = str(request.GET.get('node', ''))
#         ct = str(request.GET.get('ct', ''))
#         timeFrame = str(request.GET.get('time', 'hour'))
#
#         stats = proxmox.nodes(node).openvz(ct).rrddata.get(timeframe=timeFrame)
#
#         text = json.dumps(stats, separators=(',', ':'))
#
#         return HttpResponse(text)
#     elif command == 'vmStats':
#         return HttpResponse("Ok")
# < p > disk - {{vm.disk}} < / p >
# < p > hastate - {{vm.hastate}} < / p >
# < p > maxcpu - {{vm.maxcpu}} < / p >
# < p > maxdisk - {{vm.maxdisk}} < / p >
# < p > maxmem - {{vm.maxmem}} < / p >
# < p > name - {{vm.name}} < / p >
# < p > time_creation - {{vm.time_creation}} < / p >
# < p > time_modify - {{vm.time_modify}} < / p >
#
# < p > diskread - {{vm.diskread}}
# < p > diskwrite - {{vm.diskwrite}}
# < p > netin - {{vm.netin}}
# < p > netout - {{vm.netout}}