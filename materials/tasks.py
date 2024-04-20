from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail

from users.models import User


@shared_task
def send_course_update_email(user_email, course_name):
    subject = 'Обновление материалов курса'
    message = f'Дорогой пользователь, материалы курса {course_name} были обновлены.'
    send_mail(subject, message, 'bobr@kurwa.kek', [user_email])


@shared_task
def check_inactive_users():
    max_inactive_period = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lte=max_inactive_period)
    inactive_users.update(is_active=False)
