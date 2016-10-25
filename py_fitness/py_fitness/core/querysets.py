from django.db import models


class PublishableQuerySet(models.QuerySet):
    def published(self):
        from django.utils import timezone
        return self.filter(~models.Q(publish_date=None)).filter(publish_date__lte=timezone.now())


class AuthorableQuerySet(models.QuerySet):
    def authored_by(self, author):
        return self.filter(
            models.Q(author__userprofile__first_name__istartswith=author) |
            models.Q(author__userprofile__last_name__istartswith=author)
        )


class EditorableQuerySet(models.QuerySet):
    def edited_by(self, editor):
        return self.filter(editor__email=editor)


class ChainableQuerySet(PublishableQuerySet, EditorableQuerySet, AuthorableQuerySet):
    pass
