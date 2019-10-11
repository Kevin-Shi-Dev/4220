from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html", {})

def upload(request):
    return render(request, "upload.html", {})

def image(request):
    return render(request, 'image.html', {})