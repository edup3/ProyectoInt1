# Generated by Django 5.0.1 on 2024-03-29 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_rename_symptoms_symptom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id_chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chatbot.chat'),
        ),
    ]
