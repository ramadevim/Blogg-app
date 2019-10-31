from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Post,Comment
from .forms import CommentForm
from django.views.generic import ListView,DetailView,FormView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)

def about(request):
    return render(request,'blog/about.html',{'title': 'About'})


class PostListview(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    is_liked = False
    form_class = CommentForm
    count_hit=True

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = context['post']
        post.views = post.views + 1
        if post.likes.filter(id=self.request.user.id).exists():
            context['is_liked'] = True
            context['total_likes'] = post.total_likes()
            context['comment'] = Comment.objects.all()
            context['form']=CommentForm
            context['forms']=True
            context.update({'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],})
        return context

    def comment_valid(request, form):
        if request.method != 'POST':
            # No comment submitted
            form = CommentForm()
        else:
            # Comment posted
            form = CommentForm(data=request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                form.save()
                return HttpResponseRedirect(reverse('blog:blog-home'))


def like_post(request):
    post = get_object_or_404(Post,pk=request.POST.get('post_id'))
    is_liked=False
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
    return HttpResponseRedirect(post.get_absolute_url())

def comment_post(request):
    post = get_object_or_404(Post,pk=request.POST.get('post_id'))
    forms=False
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        forms=False
    else:
        post.likes.add(request.user)
        forms=True
    return HttpResponseRedirect(post.get_absolute_url())

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

