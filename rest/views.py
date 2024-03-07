from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
import time


@api_view(["GET"])
def get_clients(request):
    return Response({"id": 1, "time": time.localtime()})


@api_view(['POST'])
def post_clients(request):
    return Response("Done")
