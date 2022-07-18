import pandas as pd
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .forms import SalesSearchForm
from .models import Sale


# Create your views here.
def home_view(request):
    sales_df = None
    positions_df = None
    form = SalesSearchForm(request.POST or None)

    if request.method == "POST":
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        chart_type = request.POST.get("chart_type")
        print(date_from, date_to, chart_type)

        sale_qs = Sale.objects.filter(
            created__date__lte=date_to, created__date__gte=date_from
        )
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        "position_id": pos.id,
                        "product": pos.product.name,
                        "quantity": pos.quantity,
                        "price": pos.price,
                        "sales_id": pos.get_sales_id(),
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            print("=====================")
            print("positions_df")
            print(positions_df)
            print("=====================")
            print("=====================")
            print("sales_df")
            print(sales_df)
            print("=====================")

        else:
            print("no data")

    context = {
        "title": "Sales",
        "form": form,
        "sales_df": sales_df,
        "positions_df": positions_df,
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
