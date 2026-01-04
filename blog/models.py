from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Post.Status.PUBLISHED, published_at__isnull=False)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Brouillon"
        PUBLISHED = "PUBLISHED", "Publié"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=240, unique=True)

    intro = models.TextField(blank=True)
    content = models.TextField()

    featured_image = models.ImageField(upload_to="posts/", blank=True, null=True)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def publish(self):
        """Passe en publié et fixe la date de publication si absente."""
        if self.status != self.Status.PUBLISHED:
            self.status = self.Status.PUBLISHED
        if not self.published_at:
            self.published_at = timezone.now()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug(self.title)
        super().save(*args, **kwargs)

    def _generate_unique_slug(self, base_text: str) -> str:
        base_slug = slugify(base_text)[:220] or "post"
        slug = base_slug
        i = 1
        while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            i += 1
            slug = f"{base_slug}-{i}"
            slug = slug[:240]
        return slug
