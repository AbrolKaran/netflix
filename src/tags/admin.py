from dataclasses import field
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin

# Register your models here.

from .models import TaggedItem

class TaggedItemInLine(GenericTabularInline): #admin.TabularInline
    model = TaggedItem
    extra = 0

class TaggedItemAdmin(admin.ModelAdmin):
    fields = ['tag', 'content_type', 'object_id', 'content_object']
    readonly_fields = ['content_object']
    class Meta:
        model =TaggedItem

admin.site.register(TaggedItem, TaggedItemAdmin)