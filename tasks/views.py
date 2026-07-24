from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib import messages
from .forms import TaskForm, RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q #Q object se hum advanced filtering kar sakte hain.

@login_required
def add_task(request):
    search = request.GET.get("search")
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added successfully.")
            return redirect('add_task')

    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user)

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    tasks = tasks.order_by("-created_at")

    context = {
        'form': form,
        'tasks': tasks
    }

    return render(request, 'tasks/add_task.html', context)

def update_task(request, id):

    task = get_object_or_404(Task,id=id,user=request.user)

    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)   #"Naya object mat banao, isi existing object ko update karo."

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task updated successfully.")
            return redirect('add_task')

    else:

        form = TaskForm(instance=task)

    context = {
        'form': form
    }

    return render(request, 'tasks/update_task.html', context)

def delete_task(request, id):

    task = get_object_or_404(Task,id=id,user=request.user)

    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect("add_task")

    context = {
        "task": task
    }

    return render(request, "tasks/delete_task.html", context)

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully.")

            return redirect("login")

    else:

        form = RegisterForm()

    context = {
        "form": form
    }

    return render(request, "tasks/register.html", context)

def login_user(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    f"Welcome {user.username}!"
                )

                return redirect("add_task")

    else:

        form = AuthenticationForm()

    context = {
        "form": form
    }

    return render(
        request,
        "tasks/login.html",
        context
    )

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")