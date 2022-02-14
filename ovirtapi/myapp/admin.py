from django.contrib import admin

# Register your models here.
from .models import User_list, VirtMashID, ResourcesProxmox


admin.site.register(User_list)
admin.site.register(VirtMashID)
admin.site.register(ResourcesProxmox)