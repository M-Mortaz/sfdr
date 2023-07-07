# Generated by Django 4.2.3 on 2023-07-07 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_remove_orderdelayreport_unique_assigned_delay_report_to_one_agent_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='orderdelayreport',
            name='unique_assigned_delay_report_to_one_agent',
        ),
        migrations.AddConstraint(
            model_name='orderdelayreport',
            constraint=models.UniqueConstraint(condition=models.Q(('agent_id__isnull', False), ('state', 2)), fields=('agent', 'state'), name='unique_assigned_delay_report_to_one_agent', violation_error_message='Agent already has an assigned delay report!'),
        ),
    ]
