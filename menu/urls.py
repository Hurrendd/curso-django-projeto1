from django.urls import path

from menu.views import view_menu

urlpatterns = [
    path('', view_menu),
]
