from django.contrib import admin
from authentication.models import User, Language


admin.site.register(Language)
admin.site.register(User)
