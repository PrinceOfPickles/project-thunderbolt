from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django_otp.plugins.otp_totp.models import TOTPDevice
import pyotp

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('index')

@login_required
def enable_otp(request):
    if request.method == 'POST':
        # Generate a new OTP secret
        secret = pyotp.random_base32()
        request.user.otp_secret = secret
        request.user.save()
        # Create a TOTP device for the user
        TOTPDevice.objects.create(user=request.user, name='default', confirmed=False)
        # Generate a QR code URL for the user to scan
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(name=request.user.email, issuer_name='EnergyDrinkReviews')
        return render(request, 'users/enable_otp.html', {'provisioning_uri': provisioning_uri})
    return render(request, 'users/enable_otp.html')

@login_required
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        secret = request.user.otp_secret
        totp = pyotp.TOTP(secret)
        if totp.verify(otp):
            # Mark the TOTP device as confirmed
            device = TOTPDevice.objects.get(user=request.user, confirmed=False)
            device.confirmed = True
            device.save()
            return redirect('profile')
    return render(request, 'users/verify_otp.html')