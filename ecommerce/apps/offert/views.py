from django.shortcuts import get_object_or_404, render
from .models import Category


def home(request):
    category_list = list(
        enumerate(Category.objects.filter(level=0).order_by('id'), start=1))
    context = {
        'category_list': category_list
    }
    return render(request, "offert/index.html", context)
