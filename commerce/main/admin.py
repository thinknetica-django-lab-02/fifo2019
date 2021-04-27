from django.contrib import admin
from django.db import models
from main.models import Product, Category, Subsciber, Tag
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget


class CreditFlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class SubsciberAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CreditFlatPageAdmin)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subsciber, SubsciberAdmin)
admin.site.register(Tag, TagAdmin)
