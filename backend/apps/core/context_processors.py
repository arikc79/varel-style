def visitor_count(request):
    try:
        from apps.core.models import SiteCounter
        return {'visitor_count': SiteCounter.get().count}
    except Exception:
        return {'visitor_count': 0}
