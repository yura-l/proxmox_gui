from django import forms

CPU_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),

)

MEM_CHOICES = (
    ("536870912", "512"),
    ("1073741824", "1Gb"),
    ("2147483648", "2Gb"),
    ("4294967296", "4Gb"),
    ("8589934592", "8Gb"),
)

HDD_CHOICES = (
    ("10737418240", "10Gb"),
    ("64424509440", "60Gb"),
    ("128849018880", "120Gb"),

)

TEMPLATE_CHOICES = (
    ("debian11", "Debian 11"),
    ("ubuntu20", "Ubuntu 20"),
    ("ubuntu16", "Ubuntu 16"),

)

class CreatevmForm(forms.Form):
    name = forms.CharField(max_length=255, label='Имя ВМ')
    # cpu = forms.ChoiceField(choices=CPU_CHOICES, label='Число CPU')
    # mem = forms.ChoiceField(choices=MEM_CHOICES, label='Объем памяти')
    # template = forms.ChoiceField(choices=TEMPLATE_CHOICES, label='ОС')
    # hdd = forms.ChoiceField(choices=HDD_CHOICES, label='Объем диска')
    # vm_hostname = forms.CharField(max_length=255, label='Full FQDN hostname')
    # vm_username = forms.CharField(max_length=255, label='VM user')
    # vm_password = forms.CharField(max_length=255, label='VM password')