from rest_framework import serializers

from models import Investor, User, Project, Task, Comment


#  https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/


class TaskInvestor(serializers.ModelSerializer):

    class Meta:
        model = Investor
        fields = ("name", )


class User(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", )


class TaskProject(serializers.ModelSerializer):

    investor = TaskInvestor()

    class Meta:
        model = Project
        fields = ("name", "investor", )


class TaskSerializer(serializers.ModelSerializer):

    user = User(read_only=True)
    editor = User()
    project = TaskProject()

    class Meta:
        model = Task
        fields = [
            'pk',
            'project',
            'add_date',
            'change_date',
            'user',
            'editor',
            'status',
            'end_date',
            'subject',
            'description',
            ]

        read_only_fields = ['pk', 'add_date', 'change_date', 'user']


class CommentSerializer(serializers.ModelSerializer):

    user = User(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'pk',
            'task',
            'user',
            'add_date',
            'description',
            ]

        read_only_fields = ['pk', 'task', 'user', 'add_date']




