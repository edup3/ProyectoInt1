# Generated by Django 5.0.2 on 2024-04-26 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_remove_message_id_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalcenter',
            name='emb',
            field=models.BinaryField(default=0),
        ),
    ]
