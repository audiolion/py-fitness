from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from core.behaviors import Authorable, Editorable, Permalinkable, Timestampable
from core.querysets import AuthorableQuerySet
from decimal import Decimal

import datetime


class Profile(Timestampable, Permalinkable):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    avatar = models.ImageField()

    url_name = "account"

    @property
    def slug_source(self):
        return self.user.username


class Measurement(Timestampable, Authorable, Permalinkable):
    profile = models.ForeignKey(Profile, related_name='profile')
    weight = models.DecimalField(max_digits=8, decimal_places=3, default=Decimal('0.000'))
    neck = models.DecimalField(max_digits=8, decimal_places=3, default=Decimal('0.000'))
    chest = models.DecimalField(max_digits=8, decimal_places=3, default=Decimal('0.000'))
    navel = models.DecimalField(max_digits=8, decimal_places=3, default=Decimal('0.000'))
    waist = models.DecimalField(max_digits=8, decimal_places=3, default=Decimal('0.000'))
    quads = models.DecimalField(max_digits=8, decimal_places=3, default=Decimal('0.000'))
    biceps = models.DecimalField(max_digits=8, decimal_places=3, default=Decimal('0.000'))
    forearms = models.DecimalField(max_digits=8, decimal_places=3, default=Decimal('0.000'))
    notes = models.TextField(blank=True)

    url_name = "measurements"

    def get_url_kwargs(self, **kwargs):
        return super(Measurement, self).get_url_kwargs(profile__slug=self.profile.slug, **kwargs)

    @property
    def slug_source(self):
        now = datetime.datetime.now()
        profile_slug = self.profile.slug
        return str(now) + '-' + profile_slug

    objects = AuthorableQuerySet.as_manager()