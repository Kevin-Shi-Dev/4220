from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from PIL import Image
from imageSearch.models import Images, Tags, ImageHasTags
import hashlib
import os
import datetime

# For uploads to save properly
module_dir = os.path.dirname(__file__)

# TODO: Split functions into different files to keep code organized
# Create your views here.
def index(request):
    return render(request, "index.html", {})

def upload(request):
    # Handle the upload
    if request.method == 'POST':
        saved_img = handle_uploaded_file(request.FILES['file'])
        image_tags = process_tags(saved_img, request.POST['tags'])
        # Uncomment print statements for web request debugging
        # print(request.POST)
        # print(saved_img)
        # TODO: Add upload success message
        # TODO: Fix redirect - doesn't work because request is sent via javascript maybe?
        return render(request, "index.html", {}) # Redirect to home page
    else:
        return render(request, "upload.html", {})

def search(request):
    # TODO: Handle a get request - maybe make a page just for searching?
    width = 0
    img_type = ""
    if request.POST['width']:
        width = int(request.POST['width'])
    if request.POST['img_type']:
        img_type = request.POST['img_type']

    # TODO: Actually search by tags - this is the more complex case
    query = Images.objects.all()
    if width > 0:
        query = query.filter(width__gte=width)
    if img_type:
        query = query.filter(image_type=img_type)

    img_names = []
    for img in query:
        img_names.append(img.image_hash + '.' + img.image_type)

    return render(request, "search_results.html", {'images': img_names})

def process_tags(img_id, t):
    tags = t.split(",")

    # TODO: VERY IMPORTANT!!! Check for tags that ALREADY EXIST and USE THAT ID!
    # This means doing a lookup before the save call and only inserting if no record is found
    for tag in tags:
        db_tag = Tags(tag_name=strip(tag),weight=0)
        db_tag.save()
        img = Images.objects.get(image_id=img_id)
        img.tags.add(db_tag)

def handle_uploaded_file(f):
    m = hashlib.md5()
    m.update(f.name.encode())
    name = m.hexdigest()
    # TODO: Check invalid mimetype / raise error to user
    img_type = get_img_type(f.content_type)
    file_path = os.path.join(module_dir, 'media', name + '.' + img_type)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # Handle thumbnail creation
    thumb_path = os.path.join(module_dir, 'media', 'thumbs', 'thumb_' + name + '.' + img_type)
    im = Image.open(file_path)

    # Retain original width / height otherwise they get modified and put in the db incorrectly
    orig_width = im.width
    orig_height = im.height
    im.thumbnail((im.width * 0.15, im.height * 0.15), Image.ANTIALIAS)
    # TODO: Change this img type depending on whether it's jpeg / png
    im.save(thumb_path, "JPEG")

    # Insert image into database, return image id
    img = Images(image_hash=name,upload_time=datetime.datetime,weight=0,width=orig_width,height=orig_height,image_type=img_type)
    img.save()

    return img.image_id

def get_img_type(mime_type):
    if mime_type == 'image/jpeg':
        return 'jpg'
    elif mime_type == 'image/png':
        return 'png'
    else:
        return ''
