from django.contrib import admin
from .models import Poll,Choice,Vote
# Register your models here.

class PollChoicInline(admin.StackedInline):
    model = Choice
    extra = 0
    max_num = 5
class PollAdmin(admin.ModelAdmin):
    inlines = [PollChoicInline]
    list_display = ['subject', 'pub_date', 'active']
    list_filter = ['subject']
    list_per_page = 20
    
admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(Vote)