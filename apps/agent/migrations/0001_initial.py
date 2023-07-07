# Generated by Django 4.2.3 on 2023-07-06 20:27

from django.db import migrations, models
import utils.fakers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=utils.fakers.fake_name, max_length=100)),
            ],
        ),
    ]