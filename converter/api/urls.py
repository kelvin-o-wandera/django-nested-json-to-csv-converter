from django.urls import path
from converter.api import views

urlpatterns = [
    path('json/', views.Index.as_view(), name='api_create'),
]



