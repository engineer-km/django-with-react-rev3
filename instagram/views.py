from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from .models import Post


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
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