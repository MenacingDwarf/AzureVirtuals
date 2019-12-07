from django.shortcuts import render, redirect
from .models import Task
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
            pass

        return redirect('/')

    return render(request, 'main/sign.html')


def hello(request):
    if request.user.is_authenticated:
        solved_tasks = Task.objects.filter(user=request.user, status="Solved")
        unsolved_tasks = Task.objects.filter(user=request.user, status="Waiting")
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
    print(len(tasks))
    if len(tasks) >= 2:
        solve_tasks()


def solve_tasks():
    subprocess.run("az vm start --name MyVm --no-wait --resource-group MyResourceGroup", shell=True)
    subprocess.run("ssh azureuser@13.90.157.122 python3 task_solution/task_solution.py exit", shell=True)
    subprocess.run("az vm stop --resource-group MyResourceGroup --name MyVm", shell=True)
