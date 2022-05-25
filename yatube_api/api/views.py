from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post, Group, Follow, User
from .serializers import (PostSerializer,
                          CommentSerializer,
                          GroupSerializer,
                          FollowSerializer)
from .permissions import AuthorPermissionOrReadOnly
from .pagination import PostPagination


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD для постов авторов.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AuthorPermissionOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def paginate_queryset(self, queryset):
        if self.request.query_params.get('limit') is None:
            return None
        return super().paginate_queryset(queryset)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD для комментариев постов.
    """
    serializer_class = CommentSerializer
    permission_classes = [AuthorPermissionOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение информации о группе/группах.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class FollowViewSet(CreateListViewSet):
    """
    Получение информации о своих подписках,
    создание новых или удаление существующих.
    """
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        following = Follow.objects.filter(user=self.request.user)
        return following

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['delete'], detail=False)
    def unfollow(self, request):
        following = get_object_or_404(User,
                                      username=request.data.get('following'))
        instance = get_object_or_404(Follow,
                                     user=request.user,
                                     following=following)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
