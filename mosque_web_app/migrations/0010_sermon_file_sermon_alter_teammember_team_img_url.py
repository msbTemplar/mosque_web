# Generated by Django 5.1.4 on 2025-01-06 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mosque_web_app', '0009_testimonial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sermon',
            name='file_sermon',
            field=models.FileField(blank=True, max_length=5500, null=True, upload_to='sermons_files/'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='team_img_url',
            field=models.ImageField(blank=True, default='path/to/default/image.jpg', max_length=5500, null=True, upload_to='team_images/'),
        ),
    ]
