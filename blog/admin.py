from django.contrib import admin
from .models import Post, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status', 'display_tag')
    list_filter = ('status', 'created', 'publish', 'author')
    filter_horizontal = ('tag',)
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


class TagInline(admin.TabularInline):
    model = Post.tag.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = (TagInline,)
    list_display = ('name', 'slug', 'display_posts')
    prepopulated_fields = {'slug': ('name',)}
