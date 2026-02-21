from django.contrib import admin
from django.db.models import Count
from .models import Category, Product, Tag
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    list_display = ("name", "slug", "product_count", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)} # works when adding new objects
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_product_count=Count("products")) # done in single query
    
    def product_count(self, obj) -> int:
        return obj._product_count # < use annotated

    # human readable 
    product_count.short_description = "Products"
    product_count.admin_order_field = "_product_count" # allows sorting in admin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for Tag model - similar pattern to CategoryAdmin."""
    
    list_display = ("name", "slug", "product_count", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    
    def get_queryset(self, request):
        """Annotate with product count to avoid N+1."""
        queryset = super().get_queryset(request)
        return queryset.annotate(_product_count=Count("products"))
    
    def product_count(self, obj) -> int:
        return obj._product_count
    
    product_count.short_description = "Products"
    product_count.admin_order_field = "_product_count"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    
    This is the main interface for creating/editing products.
    """
    # Columns in list view
    list_display = ("name", "category", "price", "is_active", "created_at")
    
    # Sidebar filters
    list_filter = ("category", "tags", "is_active", "created_at")
    
    # 1 query with JOIN
    list_select_related = ("category",)
    
    # Search box searches these fields
    search_fields = ("name", "description")
    
    # Editable directly in list view
    list_editable = ("is_active",)
    
    # Auto-populate slug from name
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    
    # Nice horizontal picker for ManyToMany (instead of Ctrl+click list)
    filter_horizontal = ("tags",)
    
    # organized into sections
    fieldsets = (
        ("Remarcable Products", {
            "fields": ("name", "slug", "description", "price")
        }),
        ("Categorization", {
            "fields": ("category", "tags")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            # "collapse" class makes this section collapsible (hidden by default)
            "classes": ("collapse",)
        }),
    )
