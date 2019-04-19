from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    mobile_no = models.CharField(max_length=10,blank=True)
    constituency = models.CharField(max_length=50)
    location = models.CharField(max_length=30 )

class Post(models.Model):

    post_status = (('nv', 'not verified'),('v','verified'),('s','solved'),('r','rejected'))
    user_post = models.ForeignKey(Profile, on_delete=models.CASCADE )
    description = models.TextField()
    area = models.TextField(null=True)
    constituency = models.CharField(max_length=50, null=True)
    problem_statement = models.CharField(max_length=70,blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    weightage = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    upvote_count = models.IntegerField(default=0)
    status_of_post = models.CharField(blank=True, choices=post_status , max_length=20)
    file_data = models.FileField( upload_to='files/', blank=True)
    alloted_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "user : %s--> problem : %s"%(self.user_post.user.username,self.problem_statement)


class Votes_Comments(models.Model):
    user_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_vote = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField()

class Photos(models.Model):
    user_post = models.ForeignKey(Post, on_delete=models.CASCADE )
    photos_post = models.ImageField(blank=True,upload_to='images/')

    def __str__(self):
        return "user : %s --> problem :%s"%(self.user_post.user_post.user.username,self.user_post.problem_statement)



# Create your models here.
