# Generated by Django 5.0.2 on 2024-04-02 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='lessons/previews/'),
        ),
    ]
