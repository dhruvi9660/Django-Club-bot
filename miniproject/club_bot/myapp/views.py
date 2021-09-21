from django.shortcuts import render,HttpResponse


def index(request):
    return render(request, 'myapp/index.html')
# Create your views here.
