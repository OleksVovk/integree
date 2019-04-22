from rest_framework import generics
from api import IsEditorOrUserReadOnly
from api.serializers import TaskSerializer, CommentSerializer
from models import Task, Comment

# Create your views here.


class TaskDetailsApiView(generics.RetrieveUpdateAPIView):

    lookup_field = 'pk'
    permission_classes = [IsEditorOrUserReadOnly]
    serializer_class = TaskSerializer

    def perform_update(self, serializer):
        serializer.save(editor=self.request.user)

    def get_queryset(self):
        return Task.objects.all()


class CommentsCreateAPIView(generics.ListCreateAPIView):

    lookup_field = 'pk'
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
