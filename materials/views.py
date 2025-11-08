from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModerator, IsOwner
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class LessonListCreateAPIView(ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), ~IsModerator()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            # Только авторизованные, но не модераторы
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            # Модераторы ИЛИ владелец
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            # Только владелец
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['list', 'retrieve']:
            # Все авторизованные
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
