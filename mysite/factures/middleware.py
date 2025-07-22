
from .models import Facture, FactureLog
from django.utils.timezone import now

class FactureLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == 'POST' and request.path.startswith('/factures/creer'):
            try:
                last_facture = Facture.objects.latest('id')
                if not FactureLog.objects.filter(facture=last_facture).exists():
                    FactureLog.objects.create(
                        facture=last_facture,
                        ip_address=self.get_client_ip(request),
                        timestamp=now()
                    )
            except Facture.DoesNotExist:
                pass 

        return response

    # Pompé en ligne -> A réécrire
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
