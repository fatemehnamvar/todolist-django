import re
from django.shortcuts import redirect, render
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages

# Create your views here.


def todolist(request):

    if request.method == 'POST':
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save()
        messages.success(request, "new task added")
        return redirect('todolist')
    else:
        task_list = TaskList.objects.all

        context = {
            'all_tasks': task_list
        }
        return render(request, 'todolist.html', context)


def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.delete()

    return redirect('todolist')


def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = True
    task.save()

    return redirect('todolist')


def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()

    return redirect('todolist')


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
