from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class API(models.Model):
    apiId = models.AutoField(primary_key=True)
    apiName = models.CharField(max_length=25)
    apiLink =models.CharField(max_length=150)

blogChoices = (
    ('Science','Science'),
    ('Technology', 'Technology'),
    ('Coding', 'Coding'),
    ('Entertaintment','Entertaintment'),

)

class BLOG(models.Model):
    blogId = models.AutoField(primary_key=True)
    blogTitle = models.CharField(max_length=80)
    blogCategory= models.CharField(max_length=150,null=True,blank=True,choices=blogChoices, default="SELECT")
    # blogDesc =models.CharField(max_length=10000)
    blogDesc = RichTextField(blank=True, null=True)
    blogImage = models.ImageField(null=True, blank=True)
    blogDate = models.DateField()
    blogSummary= models.CharField(max_length=200)

class NOTE(models.Model):
    noteId = models.AutoField(primary_key= True)
    noteTitle= models.CharField(max_length=50)
    noteDate = models.DateField()
    noteDesc= models.CharField(max_length=1000)