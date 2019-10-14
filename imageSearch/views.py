from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from PIL import Image
import logging
import hashlib
import os

# For debugging
logger = logging.getLogger(__name__)

# For uploads
module_dir = os.path.dirname(__file__)

# Create your views here.
def index(request):
    return render(request, "index.html", {})

def upload(request):
    # Handle the upload
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'])
        print(request.POST)
        # TODO: Add upload success message
        return render(request, "index.html", {}) # Redirect to home page
    else:
        return render(request, "upload.html", {})

# TODO: return image id
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
    im.thumbnail((im.width * 0.15, im.height * 0.15), Image.ANTIALIAS)
    # TODO: Change this img type depending on whether it's jpeg / png
    im.save(thumb_path, "JPEG")

def get_img_type(mime_type):
    if mime_type == 'image/jpeg':
        return 'jpg'
    elif mime_type == 'image/png':
        return 'png'
    else:
        return ''
