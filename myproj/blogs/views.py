from django.views.decorators.http import require_POST
from django.shortcuts import render , redirect , get_object_or_404
from .models import Comment , Blog , Category , Tag
from .forms import CommentForm , BlogForm
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q
from django.template.defaultfilters import slugify

def blogs_by_category(request):
    category = get_object_or_404(Category,slug=slug)
    blogs = Blog.objects.filter(category=category)

def blogs_by_tag(request):
    tag = get_object_or_404(Tag,slug=slug)
    blogs = Blog.objects.filter(tag=tag)


def blogs_list(request):
    query = request.GET.get('q','')
    category_slug = request.GET.get('category','')
    tag_slug = request.GET.get('tag','')

    blog_list = Blog.objects.all().order_by('-date')

    if query :
        blog_list = Blog.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by('-date')

    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        blog_list = blog_list.filter(category=category).order_by('-date')

    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        blog_list = blog_list.filter(tag=tag).order_by('-date')

    paginator = Paginator(blog_list, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    search_query = request.GET.get('q','')
    return render(request, 'blogs/blogs_list.html', {
        'object_list': page_obj.object_list,
        'page_obj': page_obj,                 
        'is_paginated': page_obj.has_other_pages(), 
        'search_query': search_query,
        'category_slug': category_slug,
        'tag_slug': tag_slug,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    })


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
    return redirect(request.META.get('HTTP_REFERER','blogs:list'))

@user_passes_test(lambda u : u.is_staff)
@login_required
def blog_new(request):
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user

            category_name = form.cleaned_data.get('category_name')
            if category_name:
                category , created = Category.objects.get_or_create(
                    name = category_name,
                    defaults={'slug': slugify(category_name)}
                )
                blog.category = category

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


class search_view(ListView):
    model = Blog
    template_name = 'blogs/blogs_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        query = self.request.GET.get("q")
        self.search_query = query

        if query:
            return Blog.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        return Blog.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.search_query 
        return context


    

























