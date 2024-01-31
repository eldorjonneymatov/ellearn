from django.contrib import admin

from apps.users.models import Profile, TemporaryUser, User

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(TemporaryUser)
