# Generated by Django 3.2.3 on 2022-05-02 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='repair_centre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_re', models.ImageField(upload_to='media')),
                ('name_re', models.CharField(max_length=40)),
                ('desc_serv', models.TextField()),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('se', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.service')),
            ],
        ),
    ]
