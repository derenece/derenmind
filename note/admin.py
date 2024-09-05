from django.contrib import admin
from .models import NoteBook, Note



# Register your models here.

# Register the Notebook model
admin.site.register(NoteBook)


# Register the Note model
admin.site.register(Note)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'subject')
