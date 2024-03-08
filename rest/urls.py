from django.urls import path
from .views import *
urlpatterns = [
    path("clients/", clients),
    path('clients/<int:id>/', client_details),
    path("clients/<int:pk>/projects", create_project),
    path("projects/", logged_in_user_projects),
]
