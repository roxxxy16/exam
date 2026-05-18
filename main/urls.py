from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('apply/', views.apply_view, name='apply'),
    path('review/<int:app_id>/', views.leave_review, name='leave_review'),
    path('manage/', views.admin_panel, name='admin_panel'),
    path('manage/<int:app_id>/status/', views.change_status, name='change_status'),
]
