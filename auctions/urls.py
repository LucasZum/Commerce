from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create", views.create_view, name="create"),
    path("new", views.create, name="new"),

    path("listing/<int:id>", views.listing, name="listing"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("del_watchlist/<int:id>", views.del_watchlist, name="del_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),

    path("add_comment", views.add_comment, name="add_comment"),

    path("bid", views.bid, name="bid"),

    path("close_auction/<int:id>", views.close_auction, name="close_auction"),

    path("categories", views.all_categories, name="all_categories"),
    path("category/<str:category>", views.category, name="category"),
]
