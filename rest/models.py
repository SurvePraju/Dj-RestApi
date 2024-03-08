from django.db import models
from django.contrib.auth.models import User


class Clients(models.Model):
    client_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    projects = models.ForeignKey("Projects", on_delete=models.CASCADE)
    created_by = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="created_client")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name


class Projects(models.Model):
    project_name = models.CharField(max_length=100)

    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="created_project")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name
