from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0002_rename_questios_questions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questions",
            name="title",
            field=models.CharField(max_length=200),
        ),
    ]
