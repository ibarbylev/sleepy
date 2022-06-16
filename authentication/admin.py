from django.contrib import admin
from authentication.models import UserProfile, Language


admin.site.register(Language)
admin.site.register(UserProfile)
