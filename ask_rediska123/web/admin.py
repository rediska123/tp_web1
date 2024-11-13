from django.contrib import admin
from .models import *

admin.site.register(profile)
admin.site.register(question)
admin.site.register(answer)
admin.site.register(tag)
admin.site.register(answerlike)
admin.site.register(questionlike)

# Register your models here.
