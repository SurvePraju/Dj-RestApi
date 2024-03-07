from django.urls import path
from .views import *
urlpatterns = [
    path("clients/", clients),
    path('clients/<int:id>/', client_details),
    path("clients/<int:id>/projects", create_project),
]
