import math

from django import template
import locale
import datetime
register = template.Library()



@register.filter(name='uptime')
def conv_uptime(value):
    locale.setlocale(locale.LC_ALL, "ru")
    return str(datetime.timedelta(seconds=value))

@register.filter(name='convert_size')
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])