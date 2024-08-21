from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, DeviceForm, UserDeviceForm
from .models import Device, UserDevice

@login_required
def new_user_device(request):
    if request.method == 'POST':
        user_device_form = UserDeviceForm(request.POST)
        device_form = DeviceForm(request.POST)

        if user_device_form.is_valid():
            if user_device_form.cleaned_data.get('new_device'):
                if device_form.is_valid():
                    new_device = device_form.save()
                    user_device = user_device_form.save(commit=False)
                    user_device.device = new_device
                    user_device.user = request.user
                    user_device.save()
                    messages.success(request, 'New device and user device added successfully!')
                else:
                    messages.error(request, 'Please correct the errors below.')
            else:
                user_device = user_device_form.save(commit=False)
                user_device.user = request.user
                user_device.save()
                messages.success(request, 'User device added successfully!')
            return redirect('devices')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_device_form = UserDeviceForm()
        device_form = DeviceForm()

    return render(request, 'new_user_device.html', {
        'user_device_form': user_device_form,
        'device_form': device_form
    })

@login_required
def devices(request):
    user_devices = UserDevice.objects.filter(user=request.user)
    all_devices = Device.objects.all()

    return render(request, 'devices.html', {
        'user_devices': user_devices,
        'all_devices': all_devices,
    })

def logout_to_login(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def update_user_info(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your user information has been updated successfully.')
            return redirect('profile')  # Redirect to the profile page or wherever appropriate
    else:
        user_form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'user_form': user_form})


@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile picture has been updated successfully.')
            return redirect('profile')  # Redirect to the profile page or wherever appropriate
    else:
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'profile.html', {'profile_form': profile_form})

