from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Device, UserDevice

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile(user=user, profile_picture=self.cleaned_data.get('profile_picture'))
            user_profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'model', 'description', 'sales_links', 'retailer', 'manufacturer']

class UserDeviceForm(forms.ModelForm):
    class Meta:
        model = UserDevice
        fields = ['device', 'purchase_date', 'purchase_location', 'purchase_price', 'purchase_link', 'notes']

    new_device = forms.BooleanField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['device'].queryset = Device.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        new_device = cleaned_data.get("new_device")
        if new_device and not self.is_valid():
            raise forms.ValidationError("Please fill out all required fields for the new device.")
        return cleaned_data
