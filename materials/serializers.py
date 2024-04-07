from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import URLValidator


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'student', 'course')


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [URLValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_amount = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, course):
        user = self.context['request'].user
        subscription = Subscription.objects.filter(course=course.id, student=user.id)
        if subscription:
            return True
        return False

    @staticmethod
    def get_lessons_amount(obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ['name', 'preview', 'description', 'lessons', 'lessons_amount', 'is_subscribed']
