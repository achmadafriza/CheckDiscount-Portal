from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

import pip._vendor.requests as requests
import hashlib

from .forms import CheckDiscountForm
import datetime

# Create your views here.
@login_required
@permission_required('user.can_make_transaction', login_url=reverse_lazy('user:redirect'))
def checkDiscount(request):
    if request.method == "POST":
        form = CheckDiscountForm(request.POST)

        if form.is_valid():
            s = f"{request.user.username}{form.cleaned_data.get('ammount')}{int(form.cleaned_data.get('time').timestamp())}{12345}"
            data = {
                "username": request.user.username,
                'ammount': form.cleaned_data.get('ammount'),
                'time': form.cleaned_data.get('time').timestamp(),
                'signature': hashlib.sha256(s.encode()).hexdigest()
            }

            apicall = requests.post('http://127.0.0.1:8080/checkdiscount', json=data)
            if apicall.status_code == 201 or apicall.status_code == 202:
                return render(request, 'transaction/success.html', {'response': apicall.json()})
            else:
                messages.error(request, "Error, contact admin")
                return render(request, 'transaction/transaction.html', {'form': form})
        else:
            messages.error(request, "Please input the correct format")
            return render(request, 'transaction/transaction.html', {'form': form})
    else:
        form = CheckDiscountForm()
        return render(request, 'transaction/transaction.html', {'form': form})