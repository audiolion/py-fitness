from django.db import models
from django.conf import settings


class Timestampable(models.Model):
    """
    An abstract base class model that provides self-updating ''created`` and ''modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Authorable(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_author")

    class Meta:
        abstract = True


class Editorable(models.Model):
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_editor", null=True)

    class Meta:
        abstract = True


class Permalinkable(models.Model):
    slug = models.SlugField()

    class Meta:
        abstract = True

    def get_url_kwargs(self, **kwargs):
        kwargs.update(getattr(self, 'url_kwargs', {}))
        return kwargs

    def get_absolute_url(self):
        url_kwargs = self.get_url_kwargs(slug=self.slug)
        return (self.url_name, (), url_kwargs)

    def pre_save(self, instance, add):
        from django.utils.text import slugify
        if not instance.slug:
            instance.slug = slugify(Self.slug_source)