from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = [
            'message',
            'is_public'
        ]


'''
1) .save 호출 할때 비교

# 1-1) form 방식으로 view
form = PostForm(request.POST)
if form.is_valid():
    post = form.save(commit=False)
    post.author = request.user
    post.ip = request.META['REMOTE_ADDR']
    post.save()
    

# 1-2) serializer 방식으로 view
serializer.is_valid(...)
serializer.save(author=request.user, request.META['REMOTE_ADDR'])
'''