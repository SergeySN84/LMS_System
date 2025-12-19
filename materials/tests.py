from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User, Subscription
from materials.models import Course, Lesson
from django.contrib.auth.models import Group


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email="user1@test.com", password="pass123"
        )
        self.user2 = User.objects.create_user(
            email="user2@test.com", password="pass123"
        )
        self.moderator = User.objects.create_user(
            email="moder@test.com", password="pass123"
        )
        moderator_group, _ = Group.objects.get_or_create(name="moderators")
        self.moderator.groups.add(moderator_group)

        self.course1 = Course.objects.create(title="Course 1", owner=self.user1)
        self.lesson_data = {
            "title": "Test Lesson",
            "description": "Test desc",
            "video_url": "https://www.youtube.com/watch?v=abc123",
            "course": self.course1.id,
        }

    def test_create_lesson_valid(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(reverse("lesson-list-create"), self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_create_lesson_invalid_url(self):
        self.client.force_authenticate(user=self.user1)
        invalid_data = self.lesson_data.copy()
        invalid_data["video_url"] = "https://vimeo.com/123"
        response = self.client.post(reverse("lesson-list-create"), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_moderator_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(reverse("lesson-list-create"), self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_update_own_lesson(self):
        lesson = Lesson.objects.create(
            title="Own lesson",
            video_url="https://youtu.be/xyz789",
            course=self.course1,
            owner=self.user1,
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(
            reverse("lesson-detail", kwargs={"pk": lesson.pk}), {"title": "Updated"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_other_lesson(self):
        lesson = Lesson.objects.create(
            title="Other lesson",
            video_url="https://youtu.be/xyz789",
            course=self.course1,
            owner=self.user2,
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(
            reverse("lesson-detail", kwargs={"pk": lesson.pk}), {"title": "Hacked"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="sub@test.com", password="pass123")
        self.course = Course.objects.create(title="Sub Course", owner=self.user)

    def test_subscribe_and_unsubscribe(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("subscribe")

        # Подписка
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # Отписка
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
