from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .forms import ContactForm
from django.core.mail import send_mail

def index(request):
    return render(request, 'myapp/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'your account has been created! you can now login!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def menupage(request):
    return render(request, 'myapp/menupage.html')
# Create your views here.

def swimmingplan(request):
    return render(request, 'myapp/swimmingplan.html')


def contact(request):
    name=''
    email=''
    comment=''


    form= ContactForm(request.POST or None) #we have imported it from forms.py
    if form.is_valid():
        name= form.cleaned_data.get("name")
        email= form.cleaned_data.get("email")
        comment=form.cleaned_data.get("comment")
        receive = 'clubbot102@gmail.com' #this is the email of the admin where all the queries are redirected to

        if request.user.is_authenticated:
            subject= str(request.user) + "'s Comment"
        else:
            subject= "New Query From Customer"


        comment= name + " with the email, " + email + ", sent the following message:\n\n" + comment;
        send_mail(subject, comment, email,[receive])


        context= {'form': form}

        return render(request, 'myapp/contact.html', context)

    else:
        context= {'form': form}
        return render(request, 'myapp/contact.html', context)

