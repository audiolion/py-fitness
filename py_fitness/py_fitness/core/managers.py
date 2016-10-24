from django.db import models


class AuthorableManager(models.Manager):
    def get_queryset(self):
        return super(AuthorableManager, self).get_queryset()

    def get_author_by_name(self, author):
        return super(AuthorableManager, self).get_queryset().filter(
            models.Q(author_first__startswith=author) | models.Q(author_last__startswith=author)
        )


class EditorableManager(models.Manager):
    def get_queryset(self):
        return super(EditorableManager, self).get_queryset()


class PublishableManager(models.Manager):
    def get_queryset(self):
        return super(PublishableManager, self).get_queryset()

    def published(self):
        from django.utils import timezone
        return super(PublishableManager, self).get_queryset().filter(
            ~models.Q(publish_date=None)).filter(publish_date__lte=timezone.now())
