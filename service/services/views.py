from django.db.models import Prefetch, F
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription, Plan
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    # client__user - див пояснення в Notions
    # select_related: для "прямих" зв'язків (ForeignKey, OneToOne),автоматично створює JOIN.
    # prefetch_related: для "зворотних" зв'язків і ManyToMany.
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch(
            'client',
            queryset=Client.objects.all().select_related('user').only('company_name',
                                                                      'user__email'),
        )
        # annotate - вираховуємо значення на рівні бази(щоб не писати ще один prefetch)
    ).annotate(price=F('service__full_price') -
                     F('service__full_price') * F('plan__discount_percent') / 100.00)
    serializer_class = SubscriptionSerializer
