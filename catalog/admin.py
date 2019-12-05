from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from catalog.models import *


class BookAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_filter = ['language', 'published']
    list_display = ['name', 'author', 'pages', 'isbn', 'parsing_date']
    list_editable = ['isbn']
    search_fields = ['description']


class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('comment',)
    list_filter = ['published', 'moderated']
    list_display = ['name', 'email', 'website', 'published', 'moderated']
    list_editable = ['moderated']
    search_fields = ['name', 'description']


# Register your models here.
admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(Character)
admin.site.register(Reviews, ReviewAdmin)
