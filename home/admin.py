from django.contrib import admin
from .models import API,BLOG,NOTE


# Register your models here.
@admin.register(API)
class APIAdmin(admin.ModelAdmin):
    list_display = ('apiId','apiName','apiLink')

@admin.register(BLOG)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blogId','blogTitle','blogCategory','blogImage','blogSummary','blogDate')

@admin.register(NOTE)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('noteId','noteTitle','noteDesc','noteDate')

