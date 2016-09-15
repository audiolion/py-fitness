from django.db import models


class AuthorableQuerySet(models.query.QuerySet):
    def authored_by(self, author):
        return self.filter(author__username=author)