from django.contrib import admin
from .models import ChatGPTResponse, Component, Computer

# Register your models here.

admin.site.register(ChatGPTResponse)
admin.site.register(Component)
admin.site.register(Computer)
