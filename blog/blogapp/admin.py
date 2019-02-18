from django.contrib import admin
from .models import *

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'update_time', 'category', 'tag']

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)