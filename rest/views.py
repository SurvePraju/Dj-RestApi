from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import Clients, Projects, User
from .serializers import ClientSerializer, ProjectSerializer, CreateProjectSerializer, GetClientSerializer

import json


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
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def client_details(request, id):
    try:
        client = Clients.objects.get(id=id)

    except ObjectDoesNotExist:
        # Clients.DoesNotExists
        return Response({"message": 'Client Not Found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":

        serialized_client = GetClientSerializer(client)

        return Response(serialized_client.data, status=status.HTTP_200_OK)

    if request.method in ["PUT", "PATCH"]:
        update_data = request.data
        update_serialized = ClientSerializer(
            client, data=update_data, context={'request': request})
        if update_serialized.is_valid():
            update_serialized.save()
            return Response(update_serialized.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        client.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', "GET"])
def create_project(request, pk):
    try:
        client = Clients.objects.get(pk=pk)
    except Clients.DoesNotExist:
        return Response({'error': 'Client not found'}, status=404)

    if request.method == "GET":
        client_data = GetClientSerializer(client)
        return Response(client_data.data)

    else:
        # Extract user IDs from request data
        user_ids = [user_data.get('id')
                    for user_data in request.data.get('users', [])]
        print(user_ids)
        # Create project data including client ID
        project_data = {
            'project_name': request.data.get('project_name'),
            'client': client.id,
            'users': user_ids
        }

        serializer = CreateProjectSerializer(data=project_data)
        if serializer.is_valid():
            print(
                "#******************************@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET"])
def logged_in_user_projects(request):
    projects = Projects.objects.filter(users=request.user)
    serialized_projects = ProjectSerializer(projects, many=True)
    return Response(serialized_projects.data)
