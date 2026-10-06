from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Questios",
            new_name="Questions",
        ),
    ]
