from django.conf.urls import include, url
from rango import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^about", views.about, name="about"),
    url("^add_category", views.add_category, name="add_category"),
    url("^category/(?P<category_name_slug>[\w\-]+)/add_page/$", views.add_page, name="add_page"),
    url("^category/(?P<category_name_slug>[\w\-]+)/$", views.category, name="category"),
    # url("^register/$", views.register, name="register"),
    # url("^login/$", views.user_login, name="login"),
    url("^restricted/$", views.restricted, name="restricted"),
    # url("^logout/$", views.user_logout, name="logout"),
]