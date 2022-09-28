from django.urls import path

from .views import MainView, ReadView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('read', ReadView.as_view(), name='read')
]