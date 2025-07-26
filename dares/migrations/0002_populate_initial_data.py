from django.db import migrations

def populate_categories(apps, schema_editor):
    Category = apps.get_model('dares', 'Category')
    CATEGORIES = [
        ('extreme', 'Extreme'),
        ('creative', 'Creative'),
        ('social', 'Social'),
        ('adventure', 'Adventure'),
    ]
    for name, _ in CATEGORIES:
        Category.objects.get_or_create(name=name)

def populate_difficulty_levels(apps, schema_editor):
    DifficultyLevel = apps.get_model('dares', 'DifficultyLevel')
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('extreme', 'Extreme'),
    ]
    for name, _ in DIFFICULTY_LEVELS:
        DifficultyLevel.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('dares', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_categories),
        migrations.RunPython(populate_difficulty_levels),
    ]