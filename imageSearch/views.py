
import base64
import codecs
import operator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from imageSearch.models import Images, Tags, ImageHasTags
from PIL import Image
import hashlib
import os
import datetime
import base64
import codecs

# For uploads to save properly
module_dir = os.path.dirname(__file__)

def index(request):
    query = Images.objects.all()
    ordred =  sorted(query, key=operator.attrgetter('weight'),reverse=True)
    img_names = []
    for img in ordred:
        #print(img.weight)
        img_names.append(img.image_hash + '.' + img.image_type)

    img1 = img_names[0]
    img2 = img_names[1]
    img3 = img_names[2]

    return render(request, "index.html", {'img1': img1,'img2': img2, 'img3' : img3})

def short(request, img_id):
    img = Images.objects.filter(image_url = img_id)[0]
    #print(img)
    tags = ", ".join(tag.tag_name for tag in img.tags.all())
    img.weight = img.weight +1
    img.save()
    return render(request, "display.html", {'img': img.image_hash +'.'+img.image_type, 'type': img.image_type, 'height': img.height, 'width': img.width, 'tags': tags, 'short_url' : img.image_url})


def display(request, img_id):
    img_hash = img_id.split('.')[0]
    img = Images.objects.filter(image_hash=img_hash)[0]

    tags = ", ".join(tag.tag_name for tag in img.tags.all())

    img.weight = img.weight + 1
    img.save()

    return render(request, "display.html", {'img': img_id, 'type': img.image_type, 'height': img.height, 'width': img.width, 'tags': tags, 'short_url' : img.image_url})

def contact(request):
    return render(request, "contact.html", {})

def gallery(request):
    if request.method == "GET":
        query = Images.objects.all()
        img_names = []
        for img in query:
            img_names.append(img.image_hash + '.' + img.image_type)

        return render(request, "gallery.html", {'images': img_names })
    # If this was a real project I'd get rid of the code duplication and make a library or something. I'm sorry!
    else:
        width = 0
        img_type = ""
        search_term = ""
        if request.POST['width']:
            width = int(request.POST['width'])
        if request.POST['img_type']:
            img_type = request.POST['img_type']
        if request.POST['search_term']:
            search_term = request.POST['search_term']

        searched_tag_id = Tags.objects.filter(tag_name=search_term)
        if not searched_tag_id and width == 0 and img_type == '':
            messages.error(request, "We couldn't find the tag '" + search_term + "'")
            return redirect("/gallery")

        query = Images.objects.all()
        if searched_tag_id:
            query = query.filter(tags__in=searched_tag_id)
        if width > 0:
            query = query.filter(width__gte=width)
        if img_type:
            query = query.filter(image_type=img_type)

        img_names = []
        for img in query:
            img_names.append(img.image_hash + '.' + img.image_type)

        return render(request, "gallery.html", {'images': img_names })


def search(request):
    width = 0
    img_type = ""
    search_term = ""
    if request.POST['width']:
        width = int(request.POST['width'])
    if request.POST['img_type']:
        img_type = request.POST['img_type']
    if request.POST['search_term']:
        search_term = request.POST['search_term']

    searched_tag_id = Tags.objects.filter(tag_name=search_term)

    if not searched_tag_id and width == 0 and img_type == '':
        messages.error(request, "We couldn't find the tag '" + search_term + "'")
        return redirect("/")


    query = Images.objects.all()
    if searched_tag_id:
        query = query.filter(tags__in=searched_tag_id)
    if width > 0:
        query = query.filter(width__gte=width)
    if img_type:
        query = query.filter(image_type=img_type)

    img_names = []
    for img in query:
        img_names.append(img.image_hash + '.' + img.image_type)

    return render(request, "search_results.html", {'images': img_names })

def upload(request):
    # Handle the upload
    if request.method == 'POST':
        saved_img = handle_uploaded_file(request.FILES['file'])
        image_tags = process_tags(saved_img.image_id, request.POST['tags'])
        message = saved_img.image_hash + '.' + saved_img.image_type
        return JsonResponse({'id':message})
    else:
        return render(request, "upload.html", {})

def process_tags(img_id, t):
    tags = [x.strip() for x in t.split(",")]
    for tag in tags:
        # Check if we have the tag already
        current_tag = Tags.objects.filter(tag_name=tag)
        if not current_tag:
            db_tag = Tags(tag_name=tag,weight=0)
            db_tag.save()
            img = Images.objects.get(image_id=img_id)
            img.tags.add(db_tag)
        else:
            # If we have the tag, we associate it with the image
            for t in current_tag:
                img = Images.objects.get(image_id=img_id)
                img.tags.add(t)

def handle_uploaded_file(f):
    m = hashlib.md5()
    m.update(f.name.encode())
    name = m.hexdigest()
    short_url = str(base64.urlsafe_b64encode(codecs.decode(name, 'hex')))[2:-3]

    #print(short_url)


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
    im.thumbnail((150,150), Image.ANTIALIAS)
    im.save(thumb_path)

    # Insert image into database, return image id
    img = Images(image_hash=name,upload_time=datetime.datetime,weight=0,width=orig_width,height=orig_height,image_type=img_type,image_url= short_url)
    img.save()

    return img

def get_img_type(mime_type):
    if mime_type == 'image/jpeg':
        return 'jpg'
    elif mime_type == 'image/png':
        return 'png'
    else:
        return ''
