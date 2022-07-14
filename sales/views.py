from django.shortcuts import render
from django.views.generic import ListView

from .models import Sale


# Create your views here.
def home_view(request):
    context = {
        "title": "Sales",
    }
    return render(request, "sales/home.html", context)


class SaleListView(ListView):
    model = Sale
    template_name = "sales/main.html"
    # context_object_name = "qs"
