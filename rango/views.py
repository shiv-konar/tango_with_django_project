from django.shortcuts import render
from .models import Category


# Create your views here.


def index(request):
    # Query the database for a list of ALL categories currently stored
    # Order the categories by no. likes in descending order
    # Retrieve the top 5 categories only - or all if less than 5
    # Place the list in our context dictionary which will be passed to the template engine

    category_list = Category.objects.order_by('-likes')[:5]
    context = {
        "categories":category_list
    }
    return render(request, 'rango/index.html', context)


def about(request):
    context = {
        "messagefromview":"You are seeing the about page",
    }
    return render(request, 'rango/about.html', context)