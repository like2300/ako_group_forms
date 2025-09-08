from django.contrib import admin

from .models import Department, Post, ContactMessage

admin.site.register(Department)
admin.site.register(Post)
admin.site.register(ContactMessage)
