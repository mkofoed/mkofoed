from django.conf import settings
from django.db import models

from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify
from taggit.managers import TaggableManager

from project.utils.slug import get_unique_slug


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField(editable=False)
    published = models.BooleanField(default=False)
    title = models.CharField(max_length=256)
    content = models.TextField(blank=True)
    summary = models.CharField(max_length=512, blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=256)
    tags = TaggableManager(blank=True)

    def save(self, *args, **kwargs):
        """
        Update timestamp on save and add slug
        """
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        return super(Post, self).save(*args, **kwargs)

    def get_markdown(self):
        return mark_safe(markdownify(self.content))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
