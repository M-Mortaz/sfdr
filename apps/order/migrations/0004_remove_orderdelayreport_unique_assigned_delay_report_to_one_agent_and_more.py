# Generated by Django 4.2.3 on 2023-07-07 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderdelayreport_unique_assigned_delay_report_to_one_agent'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='orderdelayreport',
            name='unique_assigned_delay_report_to_one_agent',
        ),
        migrations.AddConstraint(
            model_name='orderdelayreport',
            constraint=models.CheckConstraint(check=models.Q(('agent_id', models.F('agent_id')), ('agent_id__isnull', False), ('state', 2)), name='unique_assigned_delay_report_to_one_agent', violation_error_message='Agent already has an assigned delay report!'),
        ),
    ]
