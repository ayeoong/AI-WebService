# Generated by Django 3.2 on 2022-11-16 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0009_auto_20221116_1342'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mypage', '0002_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('kind', models.IntegerField(default=0)),
                ('art', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_art', to='salon.artuploadmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
