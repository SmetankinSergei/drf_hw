from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import PagePagination
from materials.permissions import IsOwner, IsModerator
from materials.serializers import CourseSerializer, LessonSerializer
from materials.stripe_service import StripeApi


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = PagePagination

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [~IsModerator, IsAuthenticated]
        elif self.action == 'retrieve' or 'list':
            permission_classes = [IsModerator | IsOwner]
        elif self.action == 'update' or 'partial_update':
            permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [~IsModerator, IsOwner]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    # permission_classes = [~IsModerator, IsAuthenticated]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = PagePagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    # permission_classes = [~IsModerator, IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        """Реализация задания через post метод"""
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)

        subscription_item = Subscription.objects.filter(student=user.id, course=course_item)

        if subscription_item.exists():
            subscription_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(student=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        course_id = kwargs.get('pk')
        course = get_object_or_404(Course, id=course_id)
        stripe = StripeApi()
        if course.price_id is None or course.product_id is None:
            price = stripe.create_product(course.name, course.price)
            course.price_id = price['id']
            course.product_id = price['product']
            course.save()
        session = stripe.create_session(course.price_id)
        return Response({'url': session.url})
