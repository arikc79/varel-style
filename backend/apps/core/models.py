from django.db import models
from django.utils import timezone


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
        cls.objects.get_or_create(pk=1)
        cls.objects.filter(pk=1).update(count=models.F('count') + 1)


class SiteVisitLog(models.Model):
    date  = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date']

    @classmethod
    def increment_today(cls):
        today = timezone.now().date()
        cls.objects.get_or_create(date=today)
        cls.objects.filter(date=today).update(count=models.F('count') + 1)

    @classmethod
    def week_total(cls):
        since = timezone.now().date() - timezone.timedelta(days=7)
        return cls.objects.filter(date__gte=since).aggregate(
            s=models.Sum('count')
        )['s'] or 0
