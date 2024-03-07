from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Clients, Projects
from .serializers import ClientSerializer, ProjectSerializer


@api_view(["GET", "POST"])
def clients(request):
    if request.method == "GET":
        all_clients = Clients.objects.all()
        serialized_data = ClientSerializer(all_clients, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    else:
        client = request.data
        serialize = ClientSerializer(data=client)
        if serialize.is_valid():
            serialize.save(created_by=request.user)
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def client_details(request, id):
    try:
        client = Clients.objects.get(id=id)
    except:
        # Clients.DoesNotExists
        return Response({"message": ' no_obj'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serialized_client = ClientSerializer(client)

        return Response(serialized_client.data, status=status.HTTP_200_OK)

    if request.method in ["PUT", "PATCH"]:
        update_data = request.data
        update_serialized = ClientSerializer(client, data=update_data)
        if update_serialized.is_valid():
            update_serialized.save()
            return Response(update_serialized.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        client.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def create_project(request, id):
    try:
        client = Clients.objects.get(id=id)
    except:
        return Response({"message": "Client Does Not Exist."}, status=404)

    project = request.data
    if not project:
        return Response({"EMPTY": "Please Provide Project Name"})
    serialized_projects = ProjectSerializer(data=project)
    if serialized_projects.is_valid():
        serialized_projects.save(created_by=request.user, client=client)
        return Response(serialized_projects.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)
