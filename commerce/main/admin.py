from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from main.models import Product, Category, Subsciber
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget


class CreditFlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "quantity", "category", "is_active", "get_html_image")
    list_display_links = ('id', 'title')
    fields = ("title", "short_desc", "description", "category", "tags", "image", "get_html_image", "price", "quantity", "discount", "is_active", "views")
    readonly_fields = ('get_html_image',)
    list_filter = ('tags',)
    exclude = ('slug',)
    actions = ['make_is_active', 'make_not_active']

    def get_html_image(self, object):
        # mark_safe - указывает чтобы не экранировать теги
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50 height=50 style='border-radius: 30px;'>")
    get_html_image.short_description = "Миниатюра"

    def make_is_active(modeladmin, request, queryset):
        queryset.update(is_active=True)
    make_is_active.short_description = "Mark selected products is active"

    def make_not_active(modeladmin, request, queryset):
        queryset.update(is_active=False)
    make_not_active.short_description = "Mark selected products not active"


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class SubsciberAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CreditFlatPageAdmin)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subsciber, SubsciberAdmin)
