from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user if 'request' in self.context else None
        if user and user.is_authenticated:
            from users.models import Subscription
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
