from django.contrib import admin
from django.contrib import admin
from files_logs.models import Action, File, FileJob

admin.site.register(Action)
admin.site.register(File)
admin.site.register(FileJob)

