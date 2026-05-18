from django.contrib import admin

from .models import Application, Profile, Review


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'birth_date')
    search_fields = ('full_name', 'user__username', 'phone')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'transport_type', 'start_date', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'transport_type', 'payment_method')
    search_fields = ('user__username', 'user__profile__full_name')
    list_editable = ('status',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'rating', 'created_at')
