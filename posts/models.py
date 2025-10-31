from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils.text import slugify

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = HTMLField()
    featured_image = models.ImageField(upload_to='posts/',blank=True,null=True)
    is_draft = models.BooleanField(default=False,verbose_name="Save as Draft")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def generate_unique_slug(self):
        base = slugify(self.title)[:200] or "post"
        slug = base
        counter = 1
        #loop through slug to find used or not
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base}-{counter}"
            counter += 1
        return slug
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args,**kwargs)
        

    def __str__(self):
        return self.title
    
