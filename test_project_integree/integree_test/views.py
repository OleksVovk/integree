from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from integree_test.forms import LoginForm, TaskForm
from integree_test.models import Task


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'main/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                if user.is_staff:
                    return redirect('/admin/')
                return redirect('/main/')
        return render(request, 'main/login.html', {'form': form})


class MainPageView(View):

    def get(self, request):
        return render(request, "main/home.html")


class NotificationPageView(View):

    def get(self, request):
        query = request.GET.get('q')
        if query:
            tasks = Task.objects.filter(subject__icontains=query)
        else:
            tasks = Task.objects.all()

        return render(request, 'main/notification.html', {'tasks': tasks})


class AddNotificationView(View):

    def get(self, request):
        form = TaskForm()
        return render(request, 'main/add_notification.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            user = request.user
            new_task = Task.objects.create(project=form.cleaned_data['project'],
                                           subject=form.cleaned_data['subject'],
                                           description=form.cleaned_data['description'],
                                           user=user
                                           )
            new_task.save()
            return redirect('/notification/')
        else:
            return render(request, 'main/add_notification.html', {'form': form})


class NotificationDetailsView(View):

    def get(self, request, **kwargs):
        try:
            idkey = request.GET['id']
            task = Task.objects.get(id=idkey)
            return render(request, "main/edit_notification.html", {'task': task})
        except KeyError:
            idkey = int(kwargs['id'])
            task = Task.objects.get(id=idkey)
            return render(request, "main/edit_notification.html", {'task': task})
