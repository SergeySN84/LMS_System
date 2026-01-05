from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .paginators import CourseLessonPagination
from users.permissions import (
    IsOwner,
    IsNotModerator,
    IsModeratorOrOwner,
    IsModeratorOrCourseOwner,
)
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .tasks import send_course_update_notification


class LessonListCreateAPIView(ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsNotModerator()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated(), IsModeratorOrOwner()]
        elif self.request.method == "DELETE":
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Lesson.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = CourseLessonPagination
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsNotModerator()]
        elif self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsModeratorOrCourseOwner()]
        elif self.action == "destroy":
            return [IsAuthenticated(), IsOwner()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        # Асинхронно запускаем рассылку
        send_course_update_notification.delay(course.id)
