from django.contrib import admin

# Register your models here.
from FirstDiango.models import Topic
from FirstDiango.models import Entry

admin.site.register(Topic)
admin.site.register(Entry)
