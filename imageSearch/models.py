from django.db import models

# Note: should've made the names singular but it's a bit late to fix it
# Create your models here.
class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_hash = models.CharField(max_length=32)
    upload_time = models.DateTimeField(auto_now_add=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.IntegerField()
    height = models.IntegerField()
    image_type = models.CharField(max_length=5)
    tags = models.ManyToManyField(Tags, through='ImageHasTags')

class Urls(models.Model):
    url_id = models.AutoField(primary_key=True)
    short_url = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    image = models.OneToOneField(Images, on_delete=models.CASCADE, to_field='image_id')

class ImageHasTags(models.Model):
    image = models.ForeignKey(Images, on_delete=models.CASCADE, to_field='image_id')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, to_field='tag_id')
