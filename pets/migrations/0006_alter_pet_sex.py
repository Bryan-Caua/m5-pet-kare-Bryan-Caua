# Generated by Django 4.1.6 on 2023-02-14 18:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0005_alter_pet_sex"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="sex",
            field=models.CharField(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female"),
                    ("Default", "Not Informed"),
                ],
                default="Default",
                max_length=20,
            ),
        ),
    ]
