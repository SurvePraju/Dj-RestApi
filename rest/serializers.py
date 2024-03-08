from rest_framework import serializers
from .models import Clients, Projects, User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ClientProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'project_name']


class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    projects = ClientProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Clients
        fields = ["id", "client_name", "created_at",
                  "created_by", "projects"]

    def get_created_by(self, obj):
        return obj.created_by.username


class CreateProjectSerializer(serializers.ModelSerializer):
    users = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = Projects
        fields = ["id", "client", 'project_name', 'users', "created_by"]

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])
        project = Projects.objects.create(**validated_data)

        # Assign users to the project
        for user_data in users_data:
            user_id = user_data.get('id')
            if user_id is not None:
                project.users.add(user_id)

        return project


class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ["id", "project_name", "created_at", "created_by"]

    def get_created_by(self, instance):
        return instance.created_by.username
