from django.contrib import admin
from .models import (Lesson, Subject, Grade, Question)

admin.site.register(Lesson)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Question)
