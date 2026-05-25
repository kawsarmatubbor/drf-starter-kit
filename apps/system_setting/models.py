from django.db import models

# Identity model
class Identity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='identity/', blank=True, null=True)
    fav_icon = models.ImageField(upload_to='identity/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
# Social media model
class SocialMedia(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    icon = models.ImageField(upload_to='social_media/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name