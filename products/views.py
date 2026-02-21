from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.views.generic import ListView

from .forms import ProductFilterForm
from .models import Product

class ProductListView(ListView):
    """
    displays a paginated list of products
    search and filter functionality

    search: name or description(case insensitive)
    filter: category, tags or both
    pagination: 10 per page
    """

    model = Product
    tempalte_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    # query optimized to prevent n+1 query, combines both 
    # category and tags, selected_related for FK, and prefect for MtM
    def get_queryset(self):
        queryset = Product.objects.filter(
            is_active=True
        ).select_related(
            "category"
        ).prefetch_related(
            "tags"
        )
        # URL example: /?search=drill&category=1&tags=2&tags=3
        search_query = self.request.GET.get("search", "").strip()
        category_id = self.request.GET.get("category", "")
        tag_ids = self.request.GET.getlist("tags")  # getlist for multiple tags
        queryset = queryset.filter( # using Q for AND OR operations, Or here incase user can't remember name of product
                Q(description__icontains=search_query) |
                Q(name__icontains=search_query)
            )
        if category_id: # single underscore, no need for JOIN since indexed
            queryset = queryset.filter(category_id=category_id)

        for tag_id in tag_ids:
            if tag_id: # double under score for AND
                queryset = queryset.filter(tags__id=tag_id)

        # many to many can create duplicate rows so distinct is used
        # i.e. PowerDrill, tags: Compact, Variable Speed.
        # if we don't do distinct, itll return the same product twice.
        return queryset.distinct()
    

   # adding extra data to template, better UX 
    def get_context_data(self, **kwargs):
        # get default context
        context = super().get_context_data(**kwargs)
        
        # Pre-populate form with current filter values from URL
        # This keeps form values when user applies filters
        initial_data = {
            "search": self.request.GET.get("search", ""),
            "category": self.request.GET.get("category", ""),
            "tags": self.request.GET.getlist("tags"),
        }
        context["filter_form"] = ProductFilterForm(initial=initial_data)
        
        # Flag to show "Clear filters" button only when filters are active
        context["active_filters"] = any(initial_data.values())
        
        return context 