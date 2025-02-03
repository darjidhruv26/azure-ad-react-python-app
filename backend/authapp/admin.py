from django.contrib import admin
from .models import UserToken

class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'blacklisted')
    list_filter = ('blacklisted',) 
    search_fields = ('user__username', 'token')  

admin.site.register(UserToken, UserTokenAdmin)
