# Generated by Django 3.2.7 on 2021-09-25 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitgraphql', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='response_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]