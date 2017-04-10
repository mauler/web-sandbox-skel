from django.contrib.auth.models import UserManager
from django.db.models import QuerySet


class UserManager(UserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def verified(self, *ar, **kw):
        return self.get_queryset().verified(*ar, **kw)


class UserQuerySet(QuerySet):
    def verified(self):
        return self.filter(verified=True)
