from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings


class User_list(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=250)
    password = models.CharField(verbose_name='Пароль', max_length=250, null=True, blank=True)
    email = models.CharField(verbose_name='Email', max_length=250, null=True, blank=True)
    account = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    balance = models.IntegerField(verbose_name='Баланс', blank=True, null=True)

    def __str__(self):
        return self.name


class VirtMashID(models.Model):
    vmid = models.IntegerField(verbose_name='vmid')
    vm_cpu = models.IntegerField(verbose_name='CPU', blank=True, null=True)
    vm_mem = models.IntegerField(verbose_name='Memory', blank=True, null=True)
    vm_hdd = models.IntegerField(verbose_name='HDD', blank=True, null=True)
    vm_lan = models.CharField(verbose_name='Lan', max_length=255, blank=True, null=True)
    time_creation = models.DateTimeField(auto_now=False, auto_now_add=True)
    time_modify = models.DateTimeField(auto_now=True, auto_now_add=False)
    price = models.IntegerField(verbose_name='Стоимость VM', blank=True, null=True)
    account = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    vm_name = models.CharField(verbose_name='Name', max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.vmid)


class ResourcesProxmox(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(verbose_name='id', help_text="ID in proxmox", max_length=255)
    type = models.CharField(verbose_name='Type', help_text="Resource type", max_length=255, blank=True, null=True)
    content = models.CharField(verbose_name='Content', help_text="Allowed storage content types (when type == storage)",
                               max_length=255, blank=True, null=True)
    cpu = models.CharField(verbose_name='CPU', help_text="CPU utilization", max_length=255, blank=True, null=True)
    disk = models.CharField(verbose_name='Disk', help_text="Used disk space in bytes", max_length=255, blank=True,
                            null=True)
    hastate = models.CharField(verbose_name='Hastate', help_text="HA service status ", max_length=255, blank=True,
                               null=True)
    level = models.CharField(verbose_name='Level', help_text="Support level", max_length=255, blank=True, null=True)
    maxcpu = models.IntegerField(verbose_name='MaxCPU', help_text="Number of available CPUs", null=True)
    maxdisk = models.IntegerField(verbose_name='MaxDisk', help_text="Storage size in bytes", null=True)
    maxmem = models.IntegerField(verbose_name='MaxMem', help_text="Number of available memory in bytes", null=True)
    mem = models.CharField(verbose_name='Mem', help_text="Used memory in bytes", max_length=255, blank=True, null=True)
    name = models.CharField(verbose_name='Name', help_text="Name of the resource", max_length=255, blank=True,
                            null=True)
    node = models.CharField(verbose_name='Node', help_text="The cluster node name", max_length=255, blank=True,
                            null=True)
    plugintype = models.CharField(verbose_name='Plugintype', help_text="More specific type, if available",
                                  max_length=255, blank=True,
                                  null=True)
    pool = models.CharField(verbose_name='Pool', help_text="The pool name", max_length=255, blank=True, null=True)
    status = models.CharField(verbose_name='Status', help_text="Resource type dependent status", max_length=255,
                              blank=True, null=True)
    storage = models.CharField(verbose_name='Storage', help_text="The storage identifier", max_length=255, blank=True,
                               null=True)
    uptime = models.PositiveIntegerField(verbose_name='Uptime', help_text="Node uptime in seconds", blank=True, null=True)
    account = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    time_creation = models.DateTimeField(auto_now=False, auto_now_add=True)
    time_modify = models.DateTimeField(auto_now=True, auto_now_add=False)
    diskread = models.CharField(verbose_name='diskread', help_text="The", max_length=255, blank=True,
                                null=True)
    diskwrite = models.CharField(verbose_name='diskwrite', help_text="The", max_length=255, blank=True,
                                 null=True)
    netin = models.CharField(verbose_name='netin', help_text="The", max_length=255, blank=True,
                             null=True)
    netout = models.CharField(verbose_name='netout', help_text="The", max_length=255, blank=True,
                              null=True)
    template = models.CharField(verbose_name='template', help_text="The", max_length=255, blank=True,
                                null=True)
    vmid = models.CharField(verbose_name='vmid', help_text="The", max_length=255, blank=True,
                            null=True)
    vm_id = models.CharField(verbose_name='vm-id', help_text="The", max_length=255, blank=True,
                             null=True)

    def __str__(self):
        return str(self.vmid)
