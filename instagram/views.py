from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post
from instagram import serializers
from .permissions import IsAuthorOrReadonly


'''
class PublicPostListAPIView(generics.ListAPIView):
    queryset = Post.objects.filter(is_public=True)
    serializer_class = PostSerializer
'''

'''
class PublicPostListAPIView(APIView):
    def get(self, request):
        qs = Post.objects.filter(is_public=True)
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)
    

public_post_list = PublicPostListAPIView.as_view()
'''

'''
@api_view(['GET'])
@permission_classes([AllowAny])
def public_post_list(request, format=None):
    qs = Post.objects.filter(is_public=True)
    serializers = PostSerializer(qs, many=True)
    return Response(serializers.data)
'''


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadonly] # 해당 viewset을 접근하기 위해서는 login 해야됨.
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['message']
    ordering_fields = ['id']  # 저렬을 허용할 필드의 화이트 리스트. 미지정시에 serializer_class에 지정된 필드들. 
    ordering = ['id']  # 디포트 정렬 지정

    def perform_create(self, serializer):
        author = self.request.user # User 모델 인스턴스 or AnonymousUser 파이썬 클래스
        ip = self.request.META['REMOTE_ADDR']
        serializer.save(author=author, ip=ip)
    
    @action(detail=False, methods=['GET'])
    def public(self, request):
        qs = self.get_queryset().filter(is_public=True)
        serializer = self.get_serializer(qs, many=True)
        # serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['PATCH'])
    def set_public(self, request, pk):
        instance = self.get_object()
        instance.is_public = True
        instance.save(update_fields=['is_public'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    '''
    def dispatch(self, request, *args, **kwargs):
        print("request.body:", request.body)  #print 비추천, logger 추천
        print("request.POST:", request.POST)  #print 비추천, logger  추천
        return super().dispatch(request, *args, **kwargs)
    '''

'''
def post_list(request):
    # request.method #=> 2개 분기
    pass


def post_detail(request):
    # request.method #=> 3개 분기
    pass
'''


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'instagram/post_detail.html'
    
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        # PostSerializer(post).data
        return Response({
            'post': post,
        })