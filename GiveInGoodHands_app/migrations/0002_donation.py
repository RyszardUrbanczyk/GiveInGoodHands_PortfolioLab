# Generated by Django 3.2 on 2021-04-20 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GiveInGoodHands_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('address', models.CharField(max_length=200)),
                ('phone_number', phone_field.models.PhoneField(max_length=31, unique=True)),
                ('city', models.CharField(max_length=200)),
                ('zip_code', models.CharField(max_length=5)),
                ('pick_up_date', models.DateTimeField(auto_now_add=True)),
                ('pick_up_time', models.DateTimeField(auto_now_add=True)),
                ('pick_up_comment', models.TextField()),
                ('categories', models.ManyToManyField(to='GiveInGoodHands_app.Category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GiveInGoodHands_app.institution')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
