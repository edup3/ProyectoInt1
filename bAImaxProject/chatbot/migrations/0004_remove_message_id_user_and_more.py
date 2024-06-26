# Generated by Django 5.0.1 on 2024-04-10 15:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_delete_symptom'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='id_user',
        ),
        migrations.RemoveField(
            model_name='medicalappointment',
            name='id_user',
        ),
        migrations.RenameField(
            model_name='medicalappointment',
            old_name='id_specialist',
            new_name='specialist',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='id_chat',
            new_name='chat',
        ),
        migrations.AddField(
            model_name='medicalappointment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
