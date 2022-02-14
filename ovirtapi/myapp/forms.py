from django import forms

from .models import VirtMashID, ResourcesProxmox

TEMPLATE_CHOICES = (
    ("debian11", "Debian 11"),
    ("ubuntu20", "Ubuntu 20"),
    ("ubuntu16", "Ubuntu 16"),

)


#
# class CreatevmForm(forms.Form):
#     name = forms.CharField(max_length=255, label='Имя ВМ')
#     cpu = forms.ChoiceField(choices=CPU_CHOICES, label='Число CPU')
#     mem = forms.ChoiceField(choices=MEM_CHOICES, label='Объем памяти')
#     # template = forms.ChoiceField(choices=TEMPLATE_CHOICES, label='ОС')
#     hdd = forms.ChoiceField(choices=HDD_CHOICES, label='Объем диска')
#     # vm_hostname = forms.CharField(max_length=255, label='Full FQDN hostname')
#     # vm_username = forms.CharField(max_length=255, label='VM user')
#     # vm_password = forms.CharField(max_length=255, label='VM password')

class CreatevmForm(forms.ModelForm):
    class Meta:
        model = ResourcesProxmox
        fields = ['name', 'maxcpu', 'maxmem', 'maxdisk']
        CPU_CHOICES = (
            ("", "Select num CPU"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),

        )

        MEM_CHOICES = (
            ("", "Select mem"),
            ("512", "512"),
            ("1024", "1Gb"),
            ("2048", "2Gb"),
            ("4096", "4Gb"),
            ("8192", "8Gb"),
        )

        HDD_CHOICES = (
            ("", "Select size HDD"),
            ("10", "10Gb"),
            ("60", "60Gb"),
            ("120", "120Gb"),

        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'maxcpu': forms.Select(choices=CPU_CHOICES, attrs={'class': 'form-control'}),
            'maxmem': forms.Select(choices=MEM_CHOICES, attrs={'class': 'form-control'}),
            'maxdisk': forms.Select(choices=HDD_CHOICES, attrs={'class': 'form-control'}),

        }
