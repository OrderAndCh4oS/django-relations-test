from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import Person, Recipient, ScheduledMail, Email


class EmailMixin:

    @classmethod
    def validate_email(cls, data):
        if data.get('uuid'):
            try:
                email = Email.objects.get(uuid=data.get('uuid'))
            except Email.DoesNotExist:
                raise ValidationError('No email with this UUID was found: %s' % data.get('uuid'))
            serializer = EmailSerializer(email, data=data)
        else:
            serializer = EmailSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    @classmethod
    def create_email(cls, validated_data):
        email_data = validated_data.pop('email')
        if email_data.get('uuid'):
            email = Email.objects.get(uuid=email_data.get('uuid'))
        else:
            email_serializer = EmailSerializer(data=email_data)
            email_serializer.is_valid()
            email_serializer.save()
            email = email_serializer.instance

        return email


class PersonMixin:

    @classmethod
    def validate_person(cls, data):
        if data.get('uuid'):
            try:
                person = Person.objects.get(uuid=data.get('uuid'))
            except Person.DoesNotExist:
                raise ValidationError('No person with this UUID was found: %s' % data.get('uuid'))
            serializer = PersonSerializer(person, data=data)
        else:
            serializer = PersonSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    @classmethod
    def create_person(cls, validated_data):
        person_data = validated_data.pop('person')
        if person_data.get('uuid'):
            person = Person.objects.get(uuid=person_data.get('uuid'))
        else:
            person_serializer = PersonSerializer(data=person_data)
            person_serializer.is_valid()
            person_serializer.save()
            person = person_serializer.instance

        return person


class RecipientsMixin:

    @classmethod
    def validate_recipients(cls, recipient_data):
        validated_recipients = []
        for recipient in recipient_data:
            serializer = RecipientSerializer(data=recipient)
            serializer.is_valid(raise_exception=True)
            validated_recipients.append(serializer.validated_data)

        return validated_recipients

    @classmethod
    def pop_recipients(cls, validated_data):
        try:
            recipient_data = validated_data.pop('recipients')
        except KeyError:
            raise ValidationError({'recipients': ['This field is required']})

        return recipient_data

    @classmethod
    def create_recipients(cls, recipients_data, scheduled_mail):
        recipients = []
        for recipient_data in recipients_data:
            serializer = RecipientSerializer(data=recipient_data)
            serializer.is_valid()
            serializer.save(scheduled_mail=scheduled_mail)
            recipients.append(serializer.instance)

        return recipients


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('uuid', 'url', 'name',)


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Email
        fields = ('uuid', 'url', 'message',)


class RecipientSerializer(
    serializers.HyperlinkedModelSerializer,
    PersonMixin
):
    person = PersonSerializer(many=False)

    class Meta:
        model = Recipient
        fields = ('uuid', 'url', 'person', 'recipient_type')

    def create(self, validated_data):
        person = self.create_person(validated_data)
        recipient = Recipient.objects.create(
            person=person,
            **validated_data
        )

        return recipient


class ScheduledMailSerializer(serializers.HyperlinkedModelSerializer, EmailMixin, RecipientsMixin):
    recipients = RecipientSerializer(many=True)
    email = EmailSerializer(many=False)

    class Meta:
        model = ScheduledMail
        fields = ('uuid', 'url', 'email', 'recipients')

    def create(self, validated_data):
        recipients_data = self.pop_recipients(validated_data)
        email = self.create_email(validated_data)
        scheduled_mail = ScheduledMail.objects.create(email=email, **validated_data)
        self.create_recipients(recipients_data, scheduled_mail)

        return scheduled_mail
