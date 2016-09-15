from __future__ import unicode_literals

from django.db import models

from .behaviors import Authorable, Editorable, Permalinkable, Timestampable
from .querysets import AuthorableQuerySet