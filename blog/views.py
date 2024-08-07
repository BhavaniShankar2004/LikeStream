from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ( ListView, DetailView  , CreateView , UpdateView, DeleteView
                                  
                                  )
from .models import Post, comment
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CommentForm
from django.urls import reverse_lazy



def home(request):
    context = {
         'posts':Post.objects.all()

    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name= 'blog/home.html'
    context_object_name='posts'
    ordering = ['-data_posted']
    paginate_by= 6

class UserPostListView(ListView):
    model = Post
    template_name= 'blog/user_posts.html'
    context_object_name='posts'
    paginate_by= 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-data_posted')



class PostDetailView(DetailView):
    model = Post
    
 
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
       form.instance.author = self.request.user
       return super().form_valid(form)
    
   

    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
       form.instance.author = self.request.user
       return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url='/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})




def search(request):
    if request.method == "POST":  
        #grad the form field input
          
        search = request.POST['search']
        #Search the database
        searched = Post.objects.filter(title__contains = search)
        
        return render(request, 'blog/search.html', {'search':search, 'searched':searched})

    else: 
        return render(request, 'blog/search.html', {})
    

def search_user(request):
    if request.method == "POST":  
        search = request.POST.get('search', '')
        # Search the database for users whose username or email contains the search term
        searched = User.objects.filter(username__icontains=search)
        
        return render(request, 'blog/search_user.html', {'search': search, 'searched': searched})

    return render(request, 'blog/search_user.html', {})



def post_likes(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user) 
        return redirect(request.META.get("HTTP_REFERER"))
    
class AddCommentView(CreateView):
    model = comment
    form_class = CommentForm
    template_name= 'blog/add_comment.html'
    def form_valid(self,form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    success_url = reverse_lazy('blog-home')


