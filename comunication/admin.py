from django.contrib import admin
from .models import Articke, Coment, ViewArticle, DeleteHistory
# Register your models here.

admin.site.register(ViewArticle)
admin.site.register(Coment)


class CommentInLine(admin.StackedInline):
    model = Coment
    extra = 0



@admin.register(Articke)
class ArtickeAdmin(admin.ModelAdmin):
    inlines = [CommentInLine]


@admin.register(DeleteHistory)
class DeleteHistoryAdmin(admin.ModelAdmin):
    list_display  = ["content"]
    readonly_fields = ["user", "content", "article", "task", "comment", "time_action", "note"]


