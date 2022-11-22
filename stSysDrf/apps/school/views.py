from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from utils.permission import *


# Create your views here.
class ClassesViewSet(ModelViewSet):
    permission_classes = [TeacherPermission]
    queryset = Classes.objects.filter(is_delete=False)
    serializer_class = ClassesSerializer
