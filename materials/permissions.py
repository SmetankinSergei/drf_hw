from rest_framework.permissions import BasePermission

from materials.models import Lesson
from users.models import UserRoles


class IsOwner(BasePermission):
    message = "Вы не являетесь владельцем"

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Lesson):
            course = obj.course
            return request.user == course.owner
        return False


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True
        return False
