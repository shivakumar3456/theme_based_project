from django.contrib import admin
from socialissue import models
admin.site.register(models.Post)
admin.site.register(models.Votes_Comments )
admin.site.register(models.Photos)
admin.site.register(models.Only_votes)
admin.site.register(models.Profile)

# Register your models here.
