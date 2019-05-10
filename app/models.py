import uuid as uuid

from django.db import models


class Person(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=10)


class Email(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    message = models.CharField(max_length=10)


class ScheduledMail(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)


class Recipient(models.Model):
    TO = 'TO'
    CC = 'CC'
    BCC = 'BCC'
    RECIPIENT_TYPES = (
        ((TO, 'to'), (CC, 'cc'), (BCC, 'bcc'))
    )
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    scheduled_mail = models.ForeignKey(ScheduledMail, on_delete=models.CASCADE, related_name='recipients')
    recipient_type = models.CharField(choices=RECIPIENT_TYPES, max_length=3, default=TO)
