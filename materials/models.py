from django.db import models
from django.db.models import CASCADE


NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=250)
    preview = models.ImageField(upload_to='courses/previews/', **NULLABLE)
    description = models.TextField()
    owner = models.ForeignKey('users.User', on_delete=CASCADE, null=True)
    price = models.PositiveIntegerField(default=0)
    price_id = models.CharField(max_length=150, **NULLABLE)
    product_id = models.CharField(max_length=150, **NULLABLE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=250)
    preview = models.ImageField(upload_to='lessons/previews/', **NULLABLE)
    description = models.TextField()
    video_url = models.URLField()
    course = models.ForeignKey(to=Course, on_delete=CASCADE, related_name='lessons')

    def __str__(self):
        return self.name


class Subscription(models.Model):
    student = models.ForeignKey('users.User', on_delete=CASCADE)
    course = models.ForeignKey(Course, on_delete=CASCADE)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f'{self.student} {self.course}'


# class StripePayment(models.Model):
#     product_id = models.CharField(max_length=150)
#     price_id = models.CharField(max_length=150)
#     course = models.ForeignKey(to=Course, on_delete=CASCADE)
