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
    image_url = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tags, through='ImageHasTags')

class ImageHasTags(models.Model):
    image = models.ForeignKey(Images, on_delete=models.CASCADE, to_field='image_id')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, to_field='tag_id')
