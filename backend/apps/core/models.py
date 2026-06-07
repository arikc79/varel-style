from django.db import models


class SiteCounter(models.Model):
    count = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'Лічильник відвідувачів'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def increment(cls):
        cls.objects.filter(pk=1).update(count=models.F('count') + 1)
