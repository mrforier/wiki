from django.urls import path


from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("addwiki", views.add, name="add"),
    path("wiki/<str:entry>", views.entry, name="entry" ),
    path("wikierror/<str:entry>", views.error, name="error"),
    path("wikisearch", views.search, name="search"),

]