from rest_framework import viewsets

from app.models import Person, Recipient, ScheduledMail, Email
from app.serializers import PersonSerializer, ScheduledMailSerializer, RecipientSerializer, EmailSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class RecipientViewSet(viewsets.ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer


class ScheduledMailViewSet(viewsets.ModelViewSet):
    queryset = ScheduledMail.objects.all()
    serializer_class = ScheduledMailSerializer

