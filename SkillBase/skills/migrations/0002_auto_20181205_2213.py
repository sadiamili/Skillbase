# Generated by Django 2.0.5 on 2018-12-05 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='likes',
            field=models.ManyToManyField(through='skills.SkillLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='skilllike',
            name='user',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_skills', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='skill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SkillPost', to=settings.AUTH_USER_MODEL),
        ),
    ]
