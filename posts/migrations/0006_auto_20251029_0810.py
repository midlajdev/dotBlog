from django.db import migrations, models
from django.utils.text import slugify

def generate_initial_slugs(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')
    for post in Post.objects.all():
        base = slugify(post.title)[:200] or "post"
        slug = base
        counter = 1
        # ensure uniqueness
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base}-{counter}"
            counter += 1
        post.slug = slug
        post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_description'),  # ✅ keep this line as is
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, blank=True, null=True),
        ),
        migrations.RunPython(generate_initial_slugs),
    ]
