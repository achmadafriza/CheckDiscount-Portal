from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import pip._vendor.requests as requests
import hashlib

from user.forms import RegistrationForm, StaffPermissionForm
from user.models import Profile
from .forms import UpdateTierForm, DeleteTierForm, CreateTierForm

# Create your views here.
@login_required
@permission_required('user.is_admin', login_url=reverse_lazy('user:redirect'))
def createTier(request):
    if request.method == "GET":
        form = CreateTierForm()
        return render(request, 'staff/createtier.html', {'form': form,})
    else:
        form = CreateTierForm(request.POST)
        if form.is_valid():
            s = f"{form.cleaned_data.get('minimumTransaction')}{form.cleaned_data.get('maximumTransaction')}" \
                + f"{form.cleaned_data.get('probability')}{form.cleaned_data.get('discount')}{12345}"
            data = {
                **form.cleaned_data,
                "signature": hashlib.sha256(s.encode()).hexdigest()
            }
            apicall = requests.post("http://127.0.0.1:8080/tier", json=data)
            messages.success(request, f"Created Tier with probability = {form.cleaned_data.get('probability')}")
            return redirect(reverse('staff:tier'))
        else:
            messages.error(request, "Please correct the fields below")
            return render(request, 'staff/createtier.html', {'form': form,})

@login_required
@permission_required('user.is_admin', login_url=reverse_lazy('user:redirect'))
def deleteTier(request):
    if request.method == "GET" and "id" in request.GET:
        apicall = requests.get('http://127.0.0.1:8080/tier', params={"id": request.GET.get('id')}).json()
        if apicall['length']:
            form = DeleteTierForm({
                'id': request.GET.get('id'),
            })
            return render(request, 'staff/deletetier.html', {
                'form': form,
                'item': apicall['items'][0],
            })
        else:
            messages(request, f"Transaction Tier with id = {request.GET.get('id')} is not found")
            return redirect(reverse('staff:tier'))
    elif request.method == "POST":
        form = DeleteTierForm(request.POST)
        if form.is_valid():
            s = f"{form.cleaned_data.get('id')}{12345}"
            apicall = requests.delete(f"http://127.0.0.1:8080/tier?id={form.cleaned_data.get('id')}&signature={hashlib.sha256(s.encode()).hexdigest()}")
            if apicall.json():
                messages.success(request, f"Successfully deleted Tier with id = {form.cleaned_data.get('id')}")
                return redirect(reverse("staff:tier"))
            else:
                messages.error(request, f"Delete unsuccessful, Tier with id = {form.cleaned_data.get('id')}")
                return redirect(reverse("staff:tier"))
        else:
            messages.error(request, "There's an unknown error, please contact Dev")
            return redirect(reverse("staff:tier"))
    else:
        return redirect(reverse("user:redirect"))

@login_required
@permission_required('user.is_admin', login_url=reverse_lazy('user:redirect'))
def updateTier(request):
    if request.method == "GET" and "id" in request.GET:
        apicall = requests.get('http://127.0.0.1:8080/tier', params={"id": request.GET.get('id')}).json()
        if apicall['length']:
            form = UpdateTierForm(apicall['items'][0])
            return render(request, 'staff/updatetier.html', {'form': form})
        else:
            messages(request, f"Transaction Tier with id = {request.GET.get('id')} is not found")
            return redirect(reverse('staff:tier'))
    elif request.method == "POST":
        form = UpdateTierForm(request.POST)
        if form.is_valid():
            data = {**form.cleaned_data,}
            s = f"{data.get('id')}{data.get('minimumTransaction')}{data.get('maximumTransaction')}{data.get('probability')}{data.get('discount')}{12345}"
            data = {
                **form.cleaned_data,
                'signature': hashlib.sha256(s.encode()).hexdigest()
            }
            apicall = requests.put('http://127.0.0.1:8080/tier', json=data)
            
            if apicall.status_code == 201:
                messages.success(request, f"Transaction Tier with id = {form.cleaned_data.get('id')} successfully updated")
                return redirect(reverse('staff:tier'))
            else:
                messages.error(request, "There's an error on the Server")
                return render(request, 'staff/updatetier.html', {'form': form})
        else:
            messages.error(request, "Please correct the field below")
            return render(request, 'staff/updatetier.html', {'form': form})
    else:
        return redirect(reverse('staff:tier'))

@login_required
@permission_required('user.is_admin', login_url=reverse_lazy('user:redirect'))
def getTier(request):
    if request.method == "GET":
        if "id" in request.GET:
            apicall = requests.get('http://127.0.0.1:8080/tier', params={"id": request.GET.get('id')}).json()
        elif "ammount" in request.GET:
            apicall = requests.get('http://127.0.0.1:8080/tier', params={"ammount": request.GET.get('ammount')}).json()
        else:
            apicall = requests.get('http://127.0.0.1:8080/tier').json()

        page = request.GET.get('page', 1)
        paginator = Paginator(apicall['items'], 10)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        data = {
            "length": apicall['length'],
            "items": items
        }
        return render(request, 'staff/tier.html', data)
    
    return redirect(reverse("user:redirect"))

@login_required
@permission_required('user.can_see_log', login_url=reverse_lazy('user:redirect'))
def getAPILogs(request):
    if request.method == "GET":
        apicall = requests.get('http://127.0.0.1:8080/apilog').json()

        page = request.GET.get('page', 1)
        paginator = Paginator(apicall['items'], 10)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        data = {
            "length": apicall['length'],
            "items": items
        }
        return render(request, 'staff/apilog.html', data)
    
    return redirect(reverse("user:redirect"))

@login_required
@permission_required('user.can_see_log', login_url=reverse_lazy('user:redirect'))
def getTransactionLogs(request):
    if request.method == "GET":
        apicall = requests.get('http://127.0.0.1:8080/discountlog').json()

        page = request.GET.get('page', 1)
        paginator = Paginator(apicall['items'], 10)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        data = {
            "length": apicall['length'],
            "items": items
        }
        return render(request, 'staff/discountlog.html', data)
    
    return redirect(reverse("user:redirect"))

@login_required
@permission_required('user.is_admin', login_url=reverse_lazy('user:redirect'))
def createAdmin(request):
    if request.method == 'POST':
        data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'username': request.POST.get('username'),
            'password1': request.POST.get('password1'),
            'password2': request.POST.get('password2'),
        }
        form = RegistrationForm(data)
        permission_form = StaffPermissionForm({'permission': request.POST.get('permission')})
        if form.is_valid() and permission_form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user.profile.phone_number = form.cleaned_data.get("phone_number")
            user.is_active = True
            user.save()

            if permission_form.cleaned_data['permission'] == 'is_admin':
                group = Group.objects.get(name='Admin')
                group.user_set.add(user)
            elif permission_form.cleaned_data['permission'] == 'is_staff':
                group = Group.objects.get(name='Staff')
                group.user_set.add(user)

            messages.success(request, f'You Have Created An Admin Account, {username}')
            return redirect(reverse("user:otp"))
    else:
        form = RegistrationForm()
        permission_form = StaffPermissionForm()

    return render(request, 'user/register.html', {
        'form' : form,
        'permission_form': permission_form
    })