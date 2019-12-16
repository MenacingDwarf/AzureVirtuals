from django.shortcuts import render, redirect
from .models import Task
from django.db.models import Q
from .serializers import TaskSerializer
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
import subprocess


def log(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['user'], password=request.POST['pass'])
        if user and user.is_active == True:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'main/log.html', {'message': 'Неверный логин или пароль'})

    return render(request, 'main/log.html')


def sign(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(username=request.POST['user'], password=request.POST['pass'])
            user.save()
        except:
            return render(request, 'main/sign.html', {'message': 'Пользователь уже зарегистрирован'})

        return redirect('/')

    return render(request, 'main/sign.html')


def hello(request):
    if request.user.is_authenticated:
        solved_tasks = Task.objects.filter(user=request.user, status="Solved").reverse()
        unsolved_tasks = Task.objects.filter(Q(user=request.user), ~Q(status="Solved")).reverse()
        solved_serializer = TaskSerializer(solved_tasks, many=True)
        unsolved_serializer = TaskSerializer(unsolved_tasks, many=True)

        return render(request, "main/index.html", {"solved_tasks": solved_serializer.data,
                                                   "unsolved_tasks": unsolved_serializer.data})
    else:
        return redirect('/sign')


def add_task(request):
    task = Task()
    task.amount = request.POST.get('amount')
    task.operation_type = request.POST.get('operation_type')
    task.user = request.user
    task.save()

    check_tasks()

    return redirect('/')


def out(request):
    logout(request)
    return redirect('/')


def check_tasks():
    tasks = Task.objects.filter(status="Waiting")
    if len(tasks) >= 5:
        for task in tasks:
            task.status = "Solving"
            task.save()
        solve_tasks()


def solve_tasks():
    subprocess.Popen("bash main/script.sh", shell=True)
