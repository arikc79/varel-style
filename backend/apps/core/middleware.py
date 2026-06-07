class VisitorCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._maybe_count(request)
        return self.get_response(request)

    def _maybe_count(self, request):
        if request.method != 'GET':
            return
        path = request.path
        # пропускаємо адмінку, API, статику
        if any(path.startswith(p) for p in ('/admin/', '/api/', '/static/', '/media/')):
            return
        # пропускаємо staff/superuser (твої відвідування)
        if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_staff:
            return
        # один раз на сесію
        if request.session.get('counted'):
            return
        try:
            from apps.core.models import SiteCounter
            SiteCounter.objects.get_or_create(pk=1)
            SiteCounter.increment()
            request.session['counted'] = True
        except Exception:
            pass
