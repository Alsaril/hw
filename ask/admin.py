# Register your models here.
from django.contrib import admin

from ask.models import Question, Tag, Answer, Profile, Like


def upper_case_name(obj):
    return obj.title.upper()


upper_case_name.short_description = 'Name'


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', upper_case_name)
    list_filter = ['author']
    search_fields = ['title']


admin.site.register(Question, ItemAdmin)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Like)
