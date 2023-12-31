# Generated by Django 4.2.1 on 2023-06-22 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_course_content_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('payment_price', models.IntegerField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.course')),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.student')),
            ],
        ),
    ]
