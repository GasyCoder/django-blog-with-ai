from django.contrib import admin
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "author", "published_at", "updated_at")
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "intro", "content")
    autocomplete_fields = ("category", "tags")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"

    fieldsets = (
        ("Contenu", {"fields": ("title", "slug", "intro", "content", "featured_image")}),
        ("Organisation", {"fields": ("category", "tags", "author")}),
        ("Publication", {"fields": ("status", "published_at")}),
    )
