from django.db.models import Q
from django.utils.translation import ugettext_lazy as _u
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, PermissionDenied
from .serializers import TaskSerializer, TaskLinkedSerializer
from .models import Task


class TaskListAPIView(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskGetUpdateView(RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'

    def retrieve(self, request, *args, **kwargs):
        task = Task.objects.get(id=self.kwargs.get("task_id"))
        if task.state == Task.INPROGRESS:
            serializer = TaskLinkedSerializer(task, context={"request": request})
        else:
            serializer = self.get_serializer(task, context={"request": request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.state != Task.NEW:
            raise NotAcceptable(_u("You can't edit task."))

        if task.state == Task.DONE:
            raise PermissionDenied(_u("Task Done"))

        serializer = self.get_serializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_u("Task updated successfully!"))
