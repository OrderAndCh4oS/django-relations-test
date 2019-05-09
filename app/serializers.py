from rest_framework import serializers

from app.models import Person, Recipient, ScheduledMail, Email


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('name',)
        read_only_fields = ('uuid', 'url')


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Email
        fields = ('message',)
        read_only_fields = ('uuid', 'url')


class RecipientSerializer(serializers.HyperlinkedModelSerializer):
    person = PersonSerializer(many=False)

    class Meta:
        model = Recipient
        fields = ('person', 'recipient_type')
        read_only_fields = ('uuid', 'url')


class ScheduledMailSerializer(serializers.HyperlinkedModelSerializer):
    recipients = RecipientSerializer(many=True)
    email = EmailSerializer(many=False)

    class Meta:
        model = ScheduledMail
        fields = ('email', 'recipients')
        read_only_fields = ('uuid', 'url')

    def create(self, validated_data):
        recipients_data = validated_data.pop('recipients')
        email_data = validated_data.pop('email')
        email = Email.objects.create(**email_data)
        scheduled_mail = ScheduledMail.objects.create(email=email, **validated_data)
        for recipient_data in recipients_data:
            person_data = recipient_data.pop('person')
            person = Person.objects.create(**person_data)
            recipient = Recipient.objects.create(person=person, **recipient_data)
            scheduled_mail.recipients.add(recipient)

        return scheduled_mail
