from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['city', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(help_text='Duration in minutes')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departing_trips', to='routes.station')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arriving_trips', to='routes.station')),
                ('passengers', models.ManyToManyField(blank=True, related_name='booked_trips', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['origin__city', 'destination__city'],
            },
        ),
    ]
