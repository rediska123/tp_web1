# Generated by Django 5.1.1 on 2024-12-25 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_answer_flag_alter_answerlike_value_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionlike',
            old_name='profile',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='questionlike',
            old_name='question',
            new_name='liked_question',
        ),
        migrations.AlterUniqueTogether(
            name='questionlike',
            unique_together={('liked_question', 'author')},
        ),
    ]
