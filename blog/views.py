from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Post, Reply
from .serializers import PostSerializer, ReplySerializer


class PostViewSet(mixins.CreateModelMixin,  # 생성
                  mixins.RetrieveModelMixin,  # 단일 항목 검색
                  mixins.ListModelMixin,  # 전체 항목 목록 검색
                  mixins.DestroyModelMixin,  # 삭제
                  viewsets.GenericViewSet):  # 기본 뷰셋 기능 제공

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ReplyViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = ReplySerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if post_id:
            return Reply.objects.filter(post_id=post_id)
        return Reply.objects.none()  # post_id가 없으면 빈 queryset 반환

    @swagger_auto_schema(tags=['replies'])
    def list(self, request, post_id=None):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['replies'])
    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['replies'])
    def retrieve(self, request, post_id=None, pk=None):
        queryset = self.get_queryset()
        reply = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(reply)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['replies'])
    def destroy(self, request, post_id=None, pk=None):
        # post_id를 가진 post를 조회
        post = get_object_or_404(Post, id=post_id)

        # 만약 post_id를 가진 post가 없으면 404를 띄워
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # post_id가 있으면, 해당 post를 가지고, reply_id를 가진 reply를 조회
        queryset = self.get_queryset()
        reply = queryset.filter(post=post, id=pk).first()

        # 만약 reply_id를 가진 reply가 있으면 500을 띄워
        if reply:
            # reply.delete()
            # return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 그렇지 않으면 404를 띄워
        return Response(status=status.HTTP_404_NOT_FOUND)
