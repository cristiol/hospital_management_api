# Generated by Django 5.1 on 2024-08-29 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assistants', '0001_initial'),
        ('doctors', '0001_initial'),
        ('treatments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_treatment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applied_treatment', to='treatments.treatment')),
                ('assistants', models.ManyToManyField(blank=True, to='assistants.assistant')),
                ('doctors', models.ManyToManyField(blank=True, to='doctors.doctor')),
                ('recommended_treatment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recommended_treatment', to='treatments.treatment')),
            ],
        ),
    ]
