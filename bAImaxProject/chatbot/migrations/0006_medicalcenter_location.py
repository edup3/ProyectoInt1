# Generated by Django 5.0.2 on 2024-04-26 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0005_medicalcenter_emb'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalcenter',
            name='location',
            field=models.CharField(max_length=255, null=True),
        ),
    ]