# Generated by Django 4.1.7 on 2023-04-02 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_progress_group_discussion'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupdiscussion',
            name='progress',
            field=models.CharField(default=1, max_length=200),
        ),
        migrations.DeleteModel(
            name='Progress',
        ),
    ]
