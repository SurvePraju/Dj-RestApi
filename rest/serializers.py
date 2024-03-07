from rest_framework.serializers import Serializer
from .models import Clients, Projects


class ClientSerializer(Serializer):
    class Meta:
        model = Clients
        fields = "__all__"


class ProjectSerializer(Serializer):
    class Meta:
        model = Projects
        fields = "__all__"
