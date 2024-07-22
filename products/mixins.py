from .models import Product
from django.views.generic import ListView


class CommonProductListViewMixin(ListView):
    model = Product
    template_name = None
    context_object_name = 'products'
    paginate_by = 3

