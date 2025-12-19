from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import Subscription


@shared_task
def send_course_update_notification(course_id):
    from materials.models import Course

    course = Course.objects.get(id=course_id)

    from django.utils import timezone
    from datetime import timedelta

    if course.updated_at < timezone.now() - timedelta(hours=4):
        return "Курс не обновлялся последние 4 часа"

    subscriptions = Subscription.objects.filter(course=course)
    emails = [sub.user.email for sub in subscriptions if sub.user.email]

    if not emails:
        return "Нет подписчиков"

    send_mail(
        subject=f"Обновление курса: {course.title}",
        message=f"Курс '{course.title}' был обновлён. Зайдите,"
                f" чтобы посмотреть новые материалы.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False,
    )
    return f"Письмо отправлено {len(emails)} подписчикам"
