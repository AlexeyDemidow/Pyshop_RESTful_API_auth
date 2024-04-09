# Generated by Django 4.2.7 on 2024-04-08 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_refreshtoken_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='refreshtoken',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
