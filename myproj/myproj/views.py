from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from blogs.utils.ollama_blog import generate_blog
from blogs.utils.category_mapper import detect_category
from blogs.models import Blog , Category
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json

def homepage(request):
    return render(request, "home.html")

@csrf_exempt
def generate_blog_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "").strip()
            if not user_input:
                return JsonResponse({"error": "No input provided"}, status=400)

            result = generate_blog(user_input)
            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@login_required
def post_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            body = data.get("body")
            author = request.user

            if not title or not body:
                return JsonResponse({"success": False, "error": "Missing title or body"}, status=400)

            # Determine the category
            category_name = detect_category(title, body)
            category_slug = slugify(category_name)

            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={"slug": category_slug}
            )

            blog = Blog.objects.create(
                title=title,
                body=body,
                category=category,
                author=author
            )

            return JsonResponse({"success": True, "blog_id": blog.id})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
