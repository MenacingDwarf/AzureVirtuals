from django.shortcuts import render
from .models import Task
from .serializers import TaskSerializer
from django.http import JsonResponse


def hello(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    print(len(tasks))
    return render(request, "main/index.html", {"tasks": serializer.data})
