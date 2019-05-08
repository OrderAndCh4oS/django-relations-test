from rest_framework import serializers

from app.models import Person, Recipient, ScheduledMail


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('url', 'uuid', 'name')


class RecipientSerializer(serializers.HyperlinkedModelSerializer):
    person = PersonSerializer(many=False)

    class Meta:
        model = Recipient
        fields = ('url', 'uuid', 'person', 'recipient_type')


class ScheduledMailSerializer(serializers.HyperlinkedModelSerializer):
    recipients = RecipientSerializer(many=True)

    class Meta:
        model = ScheduledMail
        fields = ('url', 'message', 'recipients')

    def create(self, validated_data):
        recipients_data = validated_data.pop('recipients')
        scheduled_mail = ScheduledMail.objects.create(**validated_data)
        for recipient_data in recipients_data:
            person_data = recipient_data.pop('person')
            person = Person.objects.create(**person_data)
            recipient = Recipient.objects.create(person=person, **recipient_data)
            scheduled_mail.recipients.add(recipient)

        return scheduled_mail
