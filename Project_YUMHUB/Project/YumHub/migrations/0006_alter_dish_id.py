# Generated by Django 5.0.4 on 2024-04-20 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("YumHub", "0005_alter_dish_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dish",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
