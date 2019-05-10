from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import Person, Recipient, ScheduledMail, Email


class EmailMixin:

    def validate_email(self, data):
        serializer = self.populate_email_serializer(data)
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def populate_email_serializer(self, data):
        if data.get('uuid'):
            email = self.get_email(data)
            serializer = EmailSerializer(email, data=data)
        else:
            serializer = EmailSerializer(data=data)

        return serializer

    @classmethod
    def get_email(cls, data):
        try:
            email = Email.objects.get(uuid=data.get('uuid'))
        except Email.DoesNotExist:
            raise ValidationError('No email with this UUID was found: %s' % data.get('uuid'))
        return email

    def get_or_create_email(self, validated_data):
        email_data = validated_data.pop('email')
        if email_data.get('uuid'):
            email = Email.objects.get(uuid=email_data.get('uuid'))
        else:
            email = self.create_email(email_data)

        return email

    @classmethod
    def create_email(cls, email_data):
        email_serializer = EmailSerializer(data=email_data)
        email_serializer.is_valid()
        email_serializer.save()
        email = email_serializer.instance
        return email


class PersonMixin:

    def validate_person(self, data):
        serializer = self.populate_person_serializer(data)
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data

    def populate_person_serializer(self, data):
        if data.get('uuid'):
            person = self.get_person(data)
            serializer = PersonSerializer(person, data=data)
        else:
            serializer = PersonSerializer(data=data)

        return serializer

    @classmethod
    def get_person(cls, data):
        try:
            person = Person.objects.get(uuid=data.get('uuid'))
        except Person.DoesNotExist:
            raise ValidationError('No person with this UUID was found: %s' % data.get('uuid'))

        return person

    def get_or_create_person(self, validated_data):
        person_data = validated_data.pop('person')
        if person_data.get('uuid'):
            person = Person.objects.get(uuid=person_data.get('uuid'))
        else:
            person = self.create_person(person_data)

        return person

    @classmethod
    def create_person(cls, person_data):
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

    def create_recipients(self, recipients_data, scheduled_mail):
        recipients = []
        for recipient_data in recipients_data:
            recipients.append(self.create_recipient(recipient_data, scheduled_mail))

        return recipients

    @classmethod
    def create_recipient(cls, recipient_data, scheduled_mail):
        serializer = RecipientSerializer(data=recipient_data)
        serializer.is_valid()
        serializer.save(scheduled_mail=scheduled_mail)

        return serializer.instance


class ValidationsMixin:

    def required_field(self, errors, initial_data, name):
        if not self.has_field(name, initial_data):
            errors[name] = 'This field is required'

    def validate_email_field(self, initial_data, name):
        if self.has_field(name, initial_data):
            validate_email(initial_data[name])

    @classmethod
    def has_field(cls, name, initial_data):
        if name in initial_data and initial_data[name] is not None:
            return True


class PersonSerializer(serializers.HyperlinkedModelSerializer, ValidationsMixin):
    class Meta:
        model = Person
        fields = ('uuid', 'url', 'name')
        extra_kwargs = {
            'uuid': {
                'validators': []
            },
            'name': {
                'required': False
            }
        }

    def validate(self, initial_data):
        if 'uuid' in initial_data.keys():
            return initial_data
        errors = {}

        self.required_field(errors, initial_data, 'name')

        if errors:
            raise ValidationError(errors)

        return initial_data


class EmailSerializer(serializers.HyperlinkedModelSerializer, ValidationsMixin):
    class Meta:
        model = Email
        fields = ('uuid', 'url', 'message')
        extra_kwargs = {
            'uuid': {
                'validators': []
            },
            'message': {
                'required': False
            }
        }

    def validate(self, initial_data):
        if 'uuid' in initial_data.keys():
            return initial_data
        errors = {}

        self.required_field(errors, initial_data, 'message')

        if errors:
            raise ValidationError(errors)

        return initial_data


class RecipientSerializer(serializers.HyperlinkedModelSerializer, PersonMixin):
    person = PersonSerializer(many=False)

    class Meta:
        model = Recipient
        fields = ('uuid', 'url', 'person', 'recipient_type')

    def create(self, validated_data):
        person = self.get_or_create_person(validated_data)
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
        email = self.get_or_create_email(validated_data)
        scheduled_mail = ScheduledMail.objects.create(email=email, **validated_data)
        self.create_recipients(recipients_data, scheduled_mail)

        return scheduled_mail
