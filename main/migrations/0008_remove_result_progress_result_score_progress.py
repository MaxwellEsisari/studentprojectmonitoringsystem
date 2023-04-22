# Generated by Django 4.1.7 on 2023-04-01 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_groupdiscussion_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='progress',
        ),
        migrations.AddField(
            model_name='result',
            name='score',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.CharField(max_length=5)),
                ('group_discussion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.groupdiscussion')),
            ],
        ),
    ]