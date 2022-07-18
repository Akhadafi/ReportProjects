import pandas as pd
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .forms import SalesSearchForm
from .models import Sale


# Create your views here.
def home_view(request):
    sales_df = None
    form = SalesSearchForm(request.POST or None)

    if request.method == "POST":
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        chart_type = request.POST.get("chart_type")
        print(date_from, date_to, chart_type)

        qs = Sale.objects.filter(
            created__date__lte=date_to, created__date__gte=date_from
        )
        if len(qs) > 0:
            print("=====================")
            sales_df = pd.DataFrame(qs.values())
            sales_df = sales_df.to_html()
            print(sales_df)
            print("=====================")

        else:
            print("no data")

    context = {
        "title": "Sales",
        "form": form,
        "sales_df": sales_df,
    }
    return render(request, "sales/home.html", context)


class SaleListView(ListView):
    model = Sale
    template_name = "sales/main.html"
    # context_object_name = "qs"


class SaleDetailView(DetailView):
    model = Sale
    template_name = "sales/detail.html"
    # context_object_name = "qs"
