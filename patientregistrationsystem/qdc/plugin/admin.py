from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import RandomForests

admin.site.register(RandomForests, SingletonModelAdmin)
