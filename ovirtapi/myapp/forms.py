from django import forms
from django.core.validators import RegexValidator
from django.forms import CharField

from .func import storage_item_iso, proxmoxer_api
from .models import ResourcesProxmox


# TEMPLATE_CHOICES = (
#     ("debian11", "Debian 11"),
#     ("ubuntu20", "Ubuntu 20"),
#     ("ubuntu16", "Ubuntu 16"),
#
# )

#
# class CreatevmForm(forms.Form):
#     name = forms.CharField(max_length=255, label='Имя ВМ'
#     cpu = forms.ChoiceField(choices=CPU_CHOICES, label='Число CPU')
#     mem = forms.ChoiceField(choices=MEM_CHOICES, label='Объем памяти')
#     # template = forms.ChoiceField(choices=TEMPLATE_CHOICES, label='ОС')
#     hdd = forms.ChoiceField(choices=HDD_CHOICES, label='Объем диска')
#     # vm_hostname = forms.CharField(max_length=255, label='Full FQDN hostname')
#     # vm_username = forms.CharField(max_length=255, label='VM user')
#     # vm_password = forms.CharField(max_length=255, label='VM password')


class CreatevmForm(forms.ModelForm):
    storage_iso_as_list = [(k, v) for k, v in storage_item_iso(proxmoxer_api()).items()]
    iso = forms.ChoiceField(choices=storage_iso_as_list, label='', widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'required' : 'True',
        }))

    class Meta:
        model = ResourcesProxmox
        fields = ['name', 'maxcpu', 'maxmem', 'maxdisk', 'iso']

        CPU_CHOICES = (
            ("", "Выберие количество ядер CPU"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),

        )

        MEM_CHOICES = (
            ("", "Максимальный обьем памяти"),
            ("512", "512"),
            ("1024", "1Gb"),
            ("2048", "2Gb"),
            ("4096", "4Gb"),
            ("8192", "8Gb"),
        )

        HDD_CHOICES = (
            ("", "Обьем  HDD"),
            ("10", "10Gb"),
            ("60", "60Gb"),
            ("120", "120Gb"),

        )
        labels = {
            'name': '',
            'maxcpu': '',
            'maxmem': '',
            'maxdisk': '',

        }
        help_texts = {k: "" for k in fields}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя ВМ'}),
            'maxcpu': forms.Select(choices=CPU_CHOICES, attrs={'class': 'form-control'}),
            'maxmem': forms.Select(choices=MEM_CHOICES, attrs={'class': 'form-control'}),
            'maxdisk': forms.Select(choices=HDD_CHOICES, attrs={'class': 'form-control'}),

        }
