# Generated by Django 3.0.6 on 2020-10-17 21:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionFramework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnid', models.IntegerField()),
                ('title', models.CharField(max_length=120)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(blank=True, max_length=1024, null=True)),
                ('content', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'promotion',
                'ordering': ('publish_date',),
            },
        ),
    ]
