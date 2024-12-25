# Generated by Django 5.1.1 on 2024-12-25 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_remove_answer_rating_remove_profile_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='flag',
            field=models.BooleanField(default=False, verbose_name='flag'),
        ),
        migrations.AlterField(
            model_name='answerlike',
            name='value',
            field=models.IntegerField(choices=[(1, 'like'), (-1, 'dislike')], default=1, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='questionlike',
            name='value',
            field=models.IntegerField(choices=[(1, 'like'), (-1, 'dislike')], default=1, verbose_name='value'),
        ),
    ]
