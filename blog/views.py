from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, UpdateView, DeleteView
from django.urls import reverse_lazy

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


class BlogDetailView(View):
  def get(self, request, pk,*args, **kwargs):
    post = get_object_or_404( Post, pk=pk )
    context={
      'post':post
    }

    return render(request, 'blog/detail.html', context)


class BlogUpdateView(UpdateView):
  model= Post
  fields=['title','content']
  template_name='blog/update.html'

  def get_success_url(self) -> str:
    pk = self.kwargs['pk']
    return reverse_lazy('blog:detail', kwargs={'pk':pk})


class BlogDeleteView(DeleteView):
  model= Post
  template_name='blog/delete.html'
  success_url = reverse_lazy('blog:home')