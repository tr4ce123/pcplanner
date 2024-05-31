from django.contrib import admin
from .models.preferences import Preferences
from .models.computer import Component, Computer
from .models.chat_response import ChatResponse


admin.site.register(Preferences)
admin.site.register(Component)
admin.site.register(Computer)
admin.site.register(ChatResponse)
