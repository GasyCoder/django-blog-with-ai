from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Category, Tag


def post_list(request):
    qs = Post.objects.published().select_related("category", "author").prefetch_related("tags")
    paginator = Paginator(qs, 6)  # 6 posts par page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/post_list.html", {"page_obj": page_obj})


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.published().select_related("category", "author").prefetch_related("tags"),
        slug=slug
    )
    return render(request, "blog/post_detail.html", {"post": post})


def posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    qs = Post.objects.published().filter(category=category).select_related("category", "author").prefetch_related("tags")
    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return render(request, "blog/post_list.html", {"page_obj": page_obj, "filter_title": f"Catégorie: {category.name}"})


def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    qs = Post.objects.published().filter(tags=tag).select_related("category", "author").prefetch_related("tags")
    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return render(request, "blog/post_list.html", {"page_obj": page_obj, "filter_title": f"Tag: {tag.name}"})
