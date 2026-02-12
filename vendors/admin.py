from django.contrib import admin
from .models import Vendor, VendorCategory, UserVendorSelection

@admin.register(VendorCategory)
class VendorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'region_sido', 'rating_display')
    search_fields = ('name', 'address')
    list_filter = ('category', 'region_sido')

    def rating_display(self, obj):
        return f"{obj.avg_rating} ({obj.review_count})"
    rating_display.short_description = "Rating"

@admin.register(UserVendorSelection)
class UserVendorSelectionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'vendor', 'status', 'created_at')
    list_filter = ('status',)
