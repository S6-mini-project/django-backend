# Generated by Django 4.0.5 on 2022-07-02 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicinebase',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
