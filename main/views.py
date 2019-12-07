from django.shortcuts import render
from .models import Task
from .serializers import TaskSerializer
from django.http import JsonResponse


def hello(request):
    solved_tasks = Task.objects.filter(user=request.user, status="Solved")
    unsolved_tasks = Task.objects.filter(user=request.user, status="Waiting")
    solved_serializer = TaskSerializer(solved_tasks, many=True)
    unsolved_serializer = TaskSerializer(unsolved_tasks, many=True)
    return render(request, "main/index.html", {"solved_tasks": solved_serializer.data,
                                               "unsolved_tasks": unsolved_serializer.data})
