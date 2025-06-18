from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Settings

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Settings)