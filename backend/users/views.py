from djoser import views as djoser_views
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializers import AvatarSerializer


User = get_user_model()


class CustomUserViewSet(djoser_views.UserViewSet):


    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_name='me',
    )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(
        methods=['put'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me/avatar',
        url_name='me-avatar',
    )
    def avatar(self, request):
        serializer = self._change_avatar(request.data)
        return Response(serializer.data)

    @avatar.mapping.delete
    def delete_avatar(self, request):
        data = request.data
        if 'avatar' not in data:
            data = {'avatar': None}
        self._change_avatar(data)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def _change_avatar(self, data):
        instance = self.get_instance()
        serializer = AvatarSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer
