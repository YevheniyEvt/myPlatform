from django.contrib import admin

from .models import Ticket, TicketRecipient, TicketComment
# Register your models here.

class TicketCommentInLine(admin.TabularInline):
    model = TicketComment
    readonly_fields = ['action_date']
    extra = 0

class RecipientInLine(admin.TabularInline):
    model = TicketRecipient
    readonly_fields = ['accepted']
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [RecipientInLine, TicketCommentInLine]
    list_display  = ["tittle", "creator"]
    readonly_fields = ['create_date']
    
