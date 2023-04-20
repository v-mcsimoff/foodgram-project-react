from django.contrib import admin

from .models import Subscription, UserFoodgram


@admin.register(UserFoodgram)
class UserFoodgramAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = (
        'email',
        'username',
        'first_name',
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    search_fields = (
        'user',
    )


# admin.site.register(UserFoodgram, UserFoodgramAdmin)
