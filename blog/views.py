from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, UserForm, CommentForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.http import HttpResponse
    
class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
class PostDetailView(DetailView):
    model = Post

@login_required(login_url='login')
def createPostView(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            instance = form.save(commit= False)
            instance.author = request.user
            instance.save()
        return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form':form})


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'    
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm

    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

@user_passes_test(lambda u: u.is_superuser)
def draftListView(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('create_date')
    context = {'posts' : posts}
    return render(request, 'blog/post_draft_list.html', context)


###############################################################################

###############################################################################

###############################################################################

@user_passes_test(lambda u: u.is_superuser)
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required(login_url='account/login')
def add_comments_to_post(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,pk=pk)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form=CommentForm()
        return render(request,'blog/comment_form.html',{'form': form, 'pk':pk})
    else:
        return redirect('post_list')

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk= pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm( data=request.POST)

        if user_form.is_valid() :
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
            return redirect('login')

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    context = {'user_form' : user_form, 'registered': registered}
    return render(request, 'registration/register.html', context)

