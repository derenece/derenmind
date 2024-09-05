from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Each user has one notebook. One notebook is associated with single user.
class NoteBook(models.Model):
    name = models.CharField(max_length=100, default='My Notebook')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notebooks', primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Notebook"



#Each note belongs to a notebook (ForeignKey with related_name='notes').
class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    notebook = models.ForeignKey(NoteBook, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    subject = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    summary = models.TextField(default='No summary provided.')
    embedding = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
