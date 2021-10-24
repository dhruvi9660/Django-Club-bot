from django.shortcuts import render,HttpResponse


def index(request):
    return render(request, 'myapp/index.html')

def register(request):
    return render(request, 'myapp/register.html')
# Create your views here.
