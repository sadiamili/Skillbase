# Generated by Django 2.0.5 on 2018-12-05 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_courselike_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='courselike',
            name='like',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
