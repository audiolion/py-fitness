from django.conf import settings
from django.db import models

from .querysets import PublishableQuerySet, AuthorableQuerySet, EditorableQuerySet


class Authorable(models.Model):
    """
    An abstract behavior representing adding an author to a model based on the
    AUTH_USER_MODEL setting.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_author"
    )

    authors = AuthorableQuerySet.as_manager()

    class Meta:
        abstract = True


class Editorable(models.Model):
    """
    An abstract behavior representing adding an editor to a model based on the
    AUTH_USER_MODEL setting.
    """
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_editor",
        blank=True,
        null=True
    )

    editors = EditorableQuerySet.as_manager()

    class Meta:
        abstract = True


class Publishable(models.Model):
    """
    An abstract behavior that can be used as a mixin to a model when a
    publishable behavior is desired. A publish_date is set through the
    publish_on method and is_published property to return if it has been
    published, timezone aware.
    """
    publish_date = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    publications = PublishableQuerySet.as_manager()

    def publish_on(self, date=None):
        from django.utils import timezone
        if not date:
            date = timezone.now()
        self.publish_date = date
        self.save()

    @property
    def is_published(self):
        from django.utils import timezone
        return self.publish_date and self.publish_date < timezone.now()


class Timestampable(models.Model):
    """
    An abstract base class model that provides self-updating ``created`` and
    ``modified`` fields. See Two Scoops of Django 1.8 6.1.3
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
