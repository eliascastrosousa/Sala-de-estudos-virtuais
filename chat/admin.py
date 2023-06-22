from django.contrib import admin
from .models import Room, Announcement, Roadmap, Document, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Announcement)
admin.site.register(Roadmap)
admin.site.register(Document)
