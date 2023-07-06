# Generated by Django 4.2.3 on 2023-07-06 18:18

from django.db import migrations, models
import faker.providers.person


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=faker.providers.person.Provider.name, max_length=100)),
            ],
        ),
    ]
