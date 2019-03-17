from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    mobile_no = models.CharField(max_length=10,blank=True)
    constituency = models.CharField(max_length=50)
    location = models.CharField(max_length=30 )

class post(models.Model):

    post_status = (('nv', 'not verified'),('v','verified'),('s','solved'))
    user_post = models.ForeignKey(Profile, on_delete=models.CASCADE )
    description = models.TextField()
    date_posted = models.DateTimeField(blank=True)
    status_of_post = models.CharField(blank=True, choices=post_status , max_length=20)
    file = models.FileField( upload_to='files/', blank=True)
    alloted_time = models.DateTimeField(blank=True)

class votes_comments(models.Model):
    user_post = models.ForeignKey(post, on_delete=models.CASCADE)
    user_vote = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField()

class photos(models.Model):
    user_post = models.ForeignKey(post, on_delete=models.CASCADE )
    photos_post = models.ImageField(blank=True,upload_to='images/')



# Create your models here.
