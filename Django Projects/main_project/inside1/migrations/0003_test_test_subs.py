# Generated by Django 4.0.1 on 2022-01-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inside1', '0002_student_subject_test_teacher_subs_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='test_subs',
            field=models.CharField(default='[0,5,6,7,9]', max_length=30),
            preserve_default=False,
        ),
    ]