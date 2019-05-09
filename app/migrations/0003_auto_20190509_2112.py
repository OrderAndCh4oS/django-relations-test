# Generated by Django 2.2.1 on 2019-05-09 21:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190509_0818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduledmail',
            name='recipients',
        ),
        migrations.AddField(
            model_name='recipient',
            name='scheduled_mail',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.ScheduledMail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='email',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='person',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='scheduledmail',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]