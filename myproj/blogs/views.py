from django.views.decorators.http import require_POST
from django.shortcuts import render , redirect , get_object_or_404
from .models import Comment , Blog
from .forms import CommentForm , BlogForm
from django.contrib.auth.decorators import login_required , user_passes_test

# Create your views here.
def blogs_list(request):
    blogs = Blog.objects.all().order_by('-date')
    return render(request,'blogs/blogs_list.html',{'blogs':blogs})

@login_required
def blog_page(request,slug):
    blog = Blog.objects.get(slug=slug)
    comments = blog.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.name = request.user.username
            comment.save()
            return redirect('blogs:blog_page',slug=slug)
    else:
        form = CommentForm()
    
    return render(request,'blogs/blog_page.html',{
        'blog' : blog,
        'comments' : comments,
        'form' : form
    })

@login_required
def upvote_blog(request,blog_id):
    blog = get_object_or_404(Blog,id=blog_id)
    user = request.user

    if user in blog.upvoted_by.all():
        blog.upvoted_by.remove(user)
    else:
        blog.upvoted_by.add(user)
    return redirect('blogs:list')

@user_passes_test(lambda u : u.is_staff)
@login_required
def blog_new(request):
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blogs:list')
    else:
        form = BlogForm()
    return render(request,'blogs/blog_new.html',{'form' : form})

@require_POST
@login_required
def edit_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk,user=request.user)
    new_text = request.POST.get('text')
    if new_text:
        comment.text = new_text
        comment.save()
        return redirect('blogs:blog_page',slug=comment.blog.slug)

@require_POST
@login_required
def delete_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk,user=request.user)
    blog_slug = comment.blog.slug
    comment.delete()
    return redirect('blogs:blog_page',slug=blog_slug)




























