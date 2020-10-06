from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone

import pip._vendor.requests as requests
import hashlib

from .forms import RegistrationForm, OTPForm
from .models import Profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user.profile.phone_number = form.cleaned_data.get("phone_number")
            user.save()

            messages.success(request, f'You Have Created An Account, {username}, please check your email for verification')

            s = username + form.cleaned_data.get('email') + '12345'
            data = {
                'username': username,
                'email': form.cleaned_data.get('email'),
                'signature': hashlib.sha256(s.encode()).hexdigest()
            }

            apicall = requests.post("http://127.0.0.1:8080/otp/create", json=data)
            if(apicall.status_code != 201):
                raise AssertionError()

            request.session['userdata'] = {
                'id': user.id,
                'username': username
            }
            return redirect(reverse("user:otp"))
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form' : form})

def checkOTP(request):
    if 'userdata' in request.session:
        userdata = request.session['userdata']
        if request.method == 'POST':
            form = OTPForm(request.POST)
            if form.is_valid():
                s = form.cleaned_data.get('otp_number') + userdata['username'] + '12345'
                data = {
                    'otpNumber': form.cleaned_data.get('otp_number'),
                    'username': userdata['username'],
                    'signature': hashlib.sha256(s.encode()).hexdigest()
                }
                apicall = requests.post('http://127.0.0.1:8080/otp/check', json=data)
                if apicall.status_code == 202:
                    user = User.objects.get(id=userdata['id'])
                    user.is_active = True
                    user.profile.updated_at = timezone.now()
                    user.save()

                    group = Group.objects.get(name='Customer')
                    group.user_set.add(user)

                    del request.session['userdata']
                    messages.success(request, message = f"User {userdata['username']} successfully validated!")
                    return redirect(reverse("user:login"))
                elif apicall.status_code == 409:
                    form = OTPForm()
                    messages.error(request, message="OTP Number is not valid!")
                    return render(request, 'user/otp.html', {'form': form})
                elif apicall.status_code == 400:
                    form = OTPForm()
                    messages.error(request, message="Error! Bad Request")
                    return render(request, 'user/otp.html', {'form': form})
        else:
            form = OTPForm()
            return render(request, 'user/otp.html', {'form': form})
    else:
        return redirect(reverse("user:register"))

@login_required
def redirect_by_permission(request):
    if request.user.has_perm('user.can_make_transaction'):
        return redirect(reverse('transaction:checkDiscount'))
    else:
        return render(request, 'user/permissionfail.html')
