
from django.contrib import admin
from .models import (
    UserProfile, 
    MasterProfile, 
    ClientProfile, 
    Category,
    Service,
    Order,
    Message,
    Review,
    FavoriteMaster, 
    FavoriteService,
    WorkPhoto
    )

admin.site.register(UserProfile)
admin.site.register(MasterProfile)
admin.site.register(ClientProfile)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Message)
admin.site.register(Review)
admin.site.register(FavoriteMaster)
admin.site.register(FavoriteService)
admin.site.register(WorkPhoto)


"""
from django.contrib import admin
from .models import UserProfile, MasterProfile, ClientProfile, Category

admin.site.register(UserProfile)
admin.site.register(MasterProfile)
admin.site.register(ClientProfile)
admin.site.register(Category)

from .models import Service
admin.site.register(Service)

from .models import Order
admin.site.register(Order)

from .models import Message
admin.site.register(Message)

from .models import Review
admin.site.register(Review)

from .models import FavoriteMaster, FavoriteService
admin.site.register(FavoriteMaster)
admin.site.register(FavoriteService)

from .models import WorkPhoto
admin.site.register(WorkPhoto)
"""