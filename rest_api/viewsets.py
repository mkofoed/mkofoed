from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from accounts.models import User
from blog.models import Post
from rest_api.serializers import UserSerializer, PostAdminSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super(UserViewSet, self).get_queryset().order_by('name', 'email')


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostAdminSerializer

    def get_queryset(self):
        return super(PostViewSet, self).get_queryset().order_by('-date_created')
