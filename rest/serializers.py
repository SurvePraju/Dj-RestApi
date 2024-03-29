from rest_framework import serializers
from .models import Clients, Projects, User


class NestedProjectSerializer(serializers.ModelSerializer):
    '''
        Nested Serializer to expose projects objects i.e id, name.
    '''
    class Meta:
        model = Projects
        fields = ["id", "project_name"]


class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Clients

        fields = ["id", "client_name", "created_at",
                  "created_by"]

    def get_created_by(self, obj):
        return obj.created_by.username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request:
            if request.method in ["PUT", "PATCH"]:
                # print(request.method)
                # Add Field updated by dynamically based on the request Method being - PUT, PATCH
                self.Meta.fields += ["updated_at"]


class GetClientSerializer(serializers.ModelSerializer):
    '''
         For method with Id --- This displays the projects associated with Clients
    '''
    created_by = serializers.SerializerMethodField()
    projects = NestedProjectSerializer(many=True)

    class Meta:
        model = Clients

        fields = ["id", "client_name", "projects", "created_at", "created_by"]

    def get_created_by(self, obj):
        return obj.created_by.username


class ProjectSerializer(serializers.ModelSerializer):
    """ 
        Project Serializer - For all the projects Assocaited with Logged in User.
    """
    created_by = serializers.SerializerMethodField()
    # users = UserSerializer(many=True)

    class Meta:
        model = Projects
        fields = ["id", "project_name",
                  "created_at", "created_by"]  # + [ "users" ]

    def get_created_by(self, instance):
        return instance.created_by.username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UsersWithIDAndNameField(serializers.RelatedField):
    # displays both name and id
    def to_representation(self, value):
        serializer = UserSerializer(value, context=self.context)
        return serializer.data

    def to_internal_value(self, data):
        try:
            user_id = data
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")


class CreateProjectSerializer(serializers.ModelSerializer):
    '''
        Create New Project and assigned already register users to the projects can be one or many. 
    '''
    users = UsersWithIDAndNameField(queryset=User.objects.all(), many=True)
    created_by = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    def get_created_by(self, instance):
        return instance.created_by.username

    def get_client(self, instance):
        return instance.client.client_name

    class Meta:
        model = Projects
        fields = ["id", "client", 'project_name', 'users', "created_by"]

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])
        project = Projects.objects.create(**validated_data)

        # Assign existing users to the project
        project.users.add(*users_data)

        return project
