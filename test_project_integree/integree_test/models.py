from django.contrib.auth import admin
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Investor(models.Model):
    name = models.CharField(max_length=30)


class Project(models.Model):
    name = models.CharField(max_length=30)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):

    NEW = 1
    IN_PROGRESS = 2
    DONE = 3
    CANCELLED = 4

    STATUS_OF_PROJECT = (
        (NEW, "New"),
        (IN_PROGRESS, "In progress"),
        (DONE, "Done"),
        (CANCELLED, "Cancelled"),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    editor = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='editor')
    status = models.IntegerField(choices=STATUS_OF_PROJECT, default=1)
    subject = models.CharField(max_length=200, default=" ")
    description = models.CharField(max_length=200, default=" ")


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, default=" ")



