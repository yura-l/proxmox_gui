from django.db import models
from django.contrib.auth.models import User

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
    vmid = models.IntegerField(verbose_name='vmid', unique=True )
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
