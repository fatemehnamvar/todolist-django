import re
from django.shortcuts import redirect, render
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def todolist(request):

    if request.method == 'POST':
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).owner = request.user
            form.save()
        messages.success(request, "new task added")
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(owner=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('page')
        all_tasks = paginator.get_page(page)

        context = {
            'all_tasks': all_tasks
        }
        return render(request, 'todolist.html', context)


@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)

    if task.owner == request.user:
        task.delete()
    else:
        messages.error(request, ("Access denied, you are not allowed!"))

    return redirect('todolist')


@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("Access denied, you are not allowed!"))

    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request, ("Access denied, you are not allowed!"))

    return redirect('todolist')


@login_required
def edit_task(request, task_id):

    if request.method == 'POST':
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()

        messages.success(request, "task edited")
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)

        context = {
            'task_obj': task_obj
        }
        return render(request, 'edit.html', context)


def contact(request):
    context = {
        'contact_key': 'welcome to contact page.'
    }
    return render(request, 'contact.html', context)


def about(request):
    context = {
        'about_key': 'welcome to about page.'
    }
    return render(request, 'about.html', context)


def index(request):
    context = {
        'index_key': 'welcome to home page.'
    }
    return render(request, 'index.html', context)
