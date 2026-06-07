def visitor_count(request):
    try:
        from apps.core.models import SiteCounter, SiteVisitLog
        return {
            'visitor_count': SiteCounter.get().count,
            'visitor_week':  SiteVisitLog.week_total(),
        }
    except Exception:
        return {'visitor_count': 0, 'visitor_week': 0}
