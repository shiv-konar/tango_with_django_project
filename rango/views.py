from django.shortcuts import render
from .models import Category, Page


# Create your views here.


def index(request):
    # Query the database for a list of ALL categories currently stored
    # Order the categories by no. likes in descending order
    # Retrieve the top 5 categories only - or all if less than 5
    # Place the list in our context dictionary which will be passed to the template engine

    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context = {
        "categories":category_list,
        "pages":pages_list
    }
    return render(request, 'rango/index.html', context)


def about(request):
    context = {
        "messagefromview":"You are seeing the about page",
    }
    return render(request, 'rango/about.html', context)


def category(request, category_name_slug):
    context = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category = category)

        context = {
            "category":category,
            "category_name":category.name,
            "pages":pages
        }
    except Category.DoesNotExist:
        pass

    return render(request, "rango/category.html", context)