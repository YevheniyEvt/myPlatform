from django.contrib import admin
from .models import Topic, Section, Links, Image, Note
# Register your models here.

admin.site.register(Image)
admin.site.register(Links)
admin.site.register(Note)

class LinksInLine(admin.TabularInline):
    model = Links
    extra = 0

class SectionInLine(admin.TabularInline):
    model = Section
    readonly_fields = ['add_date']
    extra = 0
    inlines = [LinksInLine]

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [SectionInLine]
    list_display  = ["name"]
    




