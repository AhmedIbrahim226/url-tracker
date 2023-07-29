from django.contrib import admin
from .models import UrlModel, ChangesStore

admin.site.register(UrlModel)
admin.site.register(ChangesStore)
