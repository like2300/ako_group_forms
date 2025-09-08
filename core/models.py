from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):   
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name




# models.py
class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages"
    )
    post = models.ForeignKey(
        Post, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages"
    )
    status = models.CharField(max_length=50 ,default='Present')  # au lieu de 'message'
    ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
