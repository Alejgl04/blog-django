from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Post
from .forms import PostCreateForm

# Create your views here.
class BlogListView(View):
  def get(self, request, *args, **kwargs):

    list_posts = Post.objects.all() 
    context={
      'list_posts': list_posts 
    }
    
    return render(request, 'blog/list.html', context)

class BlogCreateView(View):
  
  def get(self, request, *args, **kwargs):
    form = PostCreateForm()

    context = {'form': form}

    return render( request, 'blog/create.html', context)

  def post(self, request):
    if request.method == 'POST':
      form = PostCreateForm( request.POST )
      if form.is_valid():
        title   = form.cleaned_data.get('title'  )
        content = form.cleaned_data.get('content')

        [post, created] = Post.objects.get_or_create( title=title, content=content )

        post.save()
        if created:
          return redirect('blog:home')
        