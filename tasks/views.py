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
from django.core.paginator import Paginator
from datetime import date
from django.db.models import Case, When, Value, IntegerField
from django.http import HttpResponse
from django.contrib.auth.models import User


@login_required
def add_task(request):
    search = request.GET.get("search")
    priority = request.GET.get("priority")
    status = request.GET.get("status")
    sort = request.GET.get("sort")
    print(status)
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

    if priority:
        tasks = tasks.filter(
        priority=priority
    )

    if status == "completed":
        tasks = tasks.filter(completed=True)

    elif status == "pending":
        tasks = tasks.filter(completed=False)    

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if sort == "oldest":
        tasks = tasks.order_by("created_at")

    elif sort == "title":
        tasks = tasks.order_by("title")

    elif sort == "due_date":
        tasks = tasks.order_by("due_date")

    elif sort == "priority":

        tasks = tasks.annotate(

            priority_order=Case(

                When(priority="High", then=Value(1)),

                When(priority="Medium", then=Value(2)),

                When(priority="Low", then=Value(3)),

                output_field=IntegerField()

                )
        ).order_by("priority_order")

    else:
        tasks = tasks.order_by("-created_at")

    paginator = Paginator(tasks, 5)   # Har page par 5 tasks

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(completed=True).count()

    pending_tasks = tasks.filter(completed=False).count()

    if total_tasks > 0:
        progress = (completed_tasks / total_tasks) * 100
    else:
        progress = 0

    today = date.today()

    high_priority_tasks = tasks.filter(
        priority="High"
    ).count()

    medium_priority_tasks = tasks.filter(
        priority="Medium"
    ).count()

    low_priority_tasks = tasks.filter(
        priority="Low"
        ).count()

    context = {
        'form': form,
        'tasks': page_obj,
        "page_obj": page_obj,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress": round(progress),
        "today": today,
        "high_priority_tasks": high_priority_tasks,
        "medium_priority_tasks": medium_priority_tasks,
        "low_priority_tasks": low_priority_tasks,
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




def create_superuser(request):
    username = "admin"
    password = "Admin@12345"
    email = "admin@example.com"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        return HttpResponse("Superuser created successfully!")

    return HttpResponse("Superuser already exists.")