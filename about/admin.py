from django.contrib import admin
from .models import (Address, Links, AboutMe,
                     Description, Tag, Projects,
                     Course, Lection, Book, Education,
                     WorkFlow, Instrument, Skills,
                     Hobbies, IconClass)
# Register your models here.

admin.site.register(Hobbies)
admin.site.register(IconClass)

class AboutMeLinksInLine(admin.TabularInline):
    model = Links
    exclude = ["project"]
    extra = 0

class AddressInLine(admin.TabularInline):
    model = Address
    extra = 0

@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    inlines = [AboutMeLinksInLine, AddressInLine]
    list_display  = ["first_name"]
    

class DescriptionInLine(admin.TabularInline):
    model = Description
    extra = 0

class ProjectsLinksInLine(admin.TabularInline):
    model = Links
    exclude = ["about"]
    extra = 0

class TagInLine(admin.TabularInline):
    model = Tag
    extra = 0

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    inlines = [ProjectsLinksInLine, TagInLine]
    list_display  = ["name"]
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [DescriptionInLine]


class CourseInLine(admin.TabularInline):
    model = Course
    extra = 0

class LectionInLine(admin.TabularInline):
    model = Lection
    extra = 0

class BookInLine(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    inlines = [CourseInLine, LectionInLine, BookInLine]



class WorkFlownInLine(admin.TabularInline):
    model = WorkFlow
    extra = 0

class InstrumentInLine(admin.TabularInline):
    model = Instrument
    extra = 0

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    inlines = [WorkFlownInLine, InstrumentInLine]



