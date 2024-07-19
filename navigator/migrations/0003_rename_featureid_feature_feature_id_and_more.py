# Generated by Django 5.0.6 on 2024-06-28 09:34

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("navigator", "0002_genre"),
    ]

    operations = [
        migrations.RenameField(
            model_name="feature",
            old_name="featureID",
            new_name="feature_id",
        ),
        migrations.RemoveField(
            model_name="feature",
            name="parentID",
        ),
        migrations.AddField(
            model_name="feature",
            name="level",
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="feature",
            name="lft",
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="feature",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="navigator.feature",
            ),
        ),
        migrations.AddField(
            model_name="feature",
            name="rght",
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="feature",
            name="tree_id",
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
    ]