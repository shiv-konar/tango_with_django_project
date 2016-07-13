from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from .models import Category, Page


# Create your views here.

#@login_required()
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
    context = {}
    return render(request, 'rango/about.html', context)


def category(request, category_name_slug):
    context = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category = category)

        context = {
            "category":category,
            "category_name":category.name,
            "pages":pages,
            "category_name_slug":category_name_slug,
        }
    except Category.DoesNotExist:
        pass

    return render(request, "rango/category.html", context)


def add_category(request):
    form = CategoryForm(request.POST or None)
    context = {
        "forms":form,
    }

    if form.is_valid():
        form.save(commit=True)

        return index(request)
    else:
        print form.errors

    return render(request, "rango/add_category.html", context)


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    form = PageForm(request.POST or None)

    if form.is_valid():
        if cat:
            page = form.save(commit=False)
            page.category = cat
            page.views = 0
            page.save()
            return category(request, category_name_slug)
    else:
        print form.errors
    context = {
        "forms":form,
        "category":cat,
    }
    return render(request, "rango/add_page.html", context)


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registraion succeeds.
    registered = False
    user_form = UserForm(data=request.POST or None)
    profile_form = UserProfileForm(data=request.POST or None)

    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.save()

        profile = profile_form.save(commit=False)
        profile.user = user

        if 'picture' in request.FILES:
            profile.picture = request.FILES["picture"]

        profile.save()

        registered = True
    else:
        print user_form.errors, profile_form.errors

    context = {
        "user_form":user_form,
        "profile_form":profile_form,
        "registered":registered,
    }
    return render(request, "rango/register.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/rango/")
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "rango/login.html", {})


@login_required()
def restricted(request):
    return render(request, 'rango/restricted.html', {})


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/rango/")
