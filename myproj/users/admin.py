from django.contrib import admin
from blogs.models import Comment
from users.models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()
# Register your models here.
admin.site.register(Comment)
admin.site.register(User,UserAdmin)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'alternate_email', 'get_backup_token']
    fields = ['user', 'alternate_email']

    def get_backup_token(self, obj):
        return obj.user.backup_token
    get_backup_token.short_description = 'Backup Token'

