# Generated by Django 2.1.2 on 2018-12-16 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0004_auto_20181209_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='level',
            field=models.CharField(choices=[('independentProficient', 'Independent/Proficient'), ('ProficientwithPrompts', 'Proficient with Prompts'), ('partiallyProficient', 'Partially Proficient'), ('notProficient', 'Not Proficient')], max_length=25, verbose_name='Level of Proficiency'),
        ),
    ]