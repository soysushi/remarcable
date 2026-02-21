from django import forms

from .models import Category, Tag

class ProductFilterForm(forms.Form):
    """regular form for viewing, not editing/creating"""
    search = forms.CharField(
        required=False,  # Optional - user doesn't have to search
        widget=forms.TextInput(attrs={
            # HTML attributes passed directly to the <input> tag
            "placeholder": "Search by description...",
            "class": "form-control",  # <- ai generated, for css bootstrap
        }),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={"class": "form-control"}), # <-- ai generated
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(), # <- ai generated suggestioin for better UI
    )
