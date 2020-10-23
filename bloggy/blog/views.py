from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone

from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model= Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        #it means from post model grab the object published_date and if published_date__lte(lte=less than or equal to current timezone then order by -published date i.e recent ones above)

class PostDetailView(DetailView):
    model=Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'

    form_class = PostForm

    model=Post

class UpdatePostView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class = PostForm
    model=Post

class DeletePostView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'
    model=Post
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

#####comments####
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request,pk):
    comment= get_object_or_404(Comment,pk=pk)
    comment.approve()
#in models u can see there is approve object that makes approve_comments True
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment= get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    #we save pk cz after deletion we need to return to detail of the post that's why we save in post_pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
