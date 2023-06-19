from django.contrib import admin

from .models import Bid, Category, Comments, Listing, User, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Bid)