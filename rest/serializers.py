from rest_framework import serializers
from .models import Clients, Projects, User


class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Clients
        fields = ["id", "client_name", "created_at",
                  "created_by", "updated_at"]

    def get_created_by(self, obj):
        return obj.created_by.username


class ProjectSerializer(serializers.Serializer):
    class Meta:
        model = Projects
        fields = ['id', 'project_name', 'client',
                  'users', 'created_at', 'created_by']
