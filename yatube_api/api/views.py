from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly, ReadOnly
from .serializers import CommentSerializer, FollowSerializer, GroupSerializer
from .serializers import PostSerializer
from posts.models import Comment, Follow, Group, Post


class PostOrGetViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated | ReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated | ReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        author = self.request.user
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=author, post=post)


class FollowViewSet(PostOrGetViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=user__username', '=following__username')

    def get_queryset(self):
        return self.request.user.follower.select_related('following')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
