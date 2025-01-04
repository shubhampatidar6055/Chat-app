from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib import messages
from .forms import *


# Create your views here.
def home_view(request):
    return render(request, "home.html")


def profile_view(request):
    profile = request.user.profile
    return render(request, "profile.html", {'profile':profile})

@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False

    return render(request, "profile_edit.html", {'form':form, 'onboarding':onboarding })

@login_required
def profile_settings(request):
    return render(request, 'profile_settings.html')

@login_required
def profile_emailchange(request):

    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, "email_form.html", {"form":form})
    
    if request.method == "POST":
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():

            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already exists')
                return redirect('profile-settings')
            form.save()

            send_email_confirmation = (request, request.user)
            return redirect('profile-settings')
        
        else:
            messages.warning(request, "Form not valid")
            return redirect('profile-settings')
    
    return redirect ('home')


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')

@login_required
def profile_delete(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "Account deleted")
        return redirect('home')

    return render(request, 'profile_delete.html')