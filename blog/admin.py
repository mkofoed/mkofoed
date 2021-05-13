from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_modified'
    fields = ('author', 'published', 'date_created', 'date_modified', 'title', 'slug', 'content', 'tags')
    readonly_fields = ('date_created', 'date_modified')
    list_display = ('title', 'slug', 'date_modified', 'published')


admin.site.register(Post, PostAdmin)
