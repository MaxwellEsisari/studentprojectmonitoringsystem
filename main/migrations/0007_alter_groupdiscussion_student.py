# Generated by Django 4.1.7 on 2023-03-31 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_groupadmin_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupdiscussion',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discussion', to='main.student'),
        ),
    ]
