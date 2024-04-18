from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from materials.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test', description='test')
        self.course.owner = self.user
        self.lesson = Lesson.objects.create(
            name='test lesson',
            description='test',
            video_url='https://www.youtube.com/test_lesson',
            course=self.course
        )

    def test_get_list(self):
        response = self.client.get(reverse('materials:lesson_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson(self):
        data = {
            'name': 'test lesson',
            'description': 'test',
            'video_url': 'https://www.youtube.com/test_lesson',
            'course': self.course.id
        }
        response = self.client.post(reverse('materials:lesson_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_lesson(self):
        response = self.client.get(reverse('materials:lesson', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        data = {
                    'name': 'new test lesson',
                    'description': 'new test',
                    'video_url': 'https://www.youtube.com/test_lesson',
                    'course': self.course.id
                }
        response = self.client.patch(reverse('materials:lesson_update', args=[self.lesson.id]), data)

        self.lesson.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])

    def test_delete_lesson(self):
        response = self.client.delete(reverse('materials:lesson_delete', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_subscription(self):
        data = {"course_id": self.course.id}
        response = self.client.post(reverse('materials:subscription'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        response = self.client.post(reverse('materials:subscription'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
