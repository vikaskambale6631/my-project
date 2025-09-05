from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Address, Medicine, Prescription

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['line1', 'line2', 'city', 'state', 'pincode', 'country', 'is_default']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'brand', 'description', 'category', 'price', 'stock', 'rx_required', 'image']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['file']