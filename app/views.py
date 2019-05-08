from rest_framework import viewsets

from app.models import Person, Recipient, ScheduledMail
from app.serializers import PersonSerializer, ScheduledMailSerializer, RecipientSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class RecipientViewSet(viewsets.ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer


class ScheduledMailViewSet(viewsets.ModelViewSet):
    queryset = ScheduledMail.objects.all()
    serializer_class = ScheduledMailSerializer

