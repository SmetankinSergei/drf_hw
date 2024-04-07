from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, \
    UserUpdateAPIView, UserDeleteAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentsListAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserCreateAPIView.as_view(), name='create'),
    path('list/', UserListAPIView.as_view(), name='list'),
    path('update/<int:pk>', UserUpdateAPIView.as_view(), name='update'),
    path('delete/<int:pk>', UserDeleteAPIView.as_view(), name='delete'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='detail'),
]
