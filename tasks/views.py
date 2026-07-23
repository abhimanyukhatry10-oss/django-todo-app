from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib import messages
from .forms import TaskForm, RegisterForm

def add_task(request):

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Task added successfully.")
            return redirect('add_task')

    else:
        form = TaskForm()

    tasks = Task.objects.all().order_by('-created_at')

    context = {
        'form': form,
        'tasks': tasks
    }

    return render(request, 'tasks/add_task.html', context)

def update_task(request, id):

    task = get_object_or_404(Task, id=id)

    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)   #"Naya object mat banao, isi existing object ko update karo."

        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('add_task')

    else:

        form = TaskForm(instance=task)

    context = {
        'form': form
    }

    return render(request, 'tasks/update_task.html', context)

def delete_task(request, id):

    task = get_object_or_404(Task, id=id)

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