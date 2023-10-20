from django import forms
from .models import Dataset
from .models import CustomUser
from .models import UserDataset



class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email Address")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@sdfi.dk'):
            raise forms.ValidationError("Email must end with '@sdfi.dk'")
        return email
    
class AdminLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterDatasetForm(forms.ModelForm):
    description = forms.CharField(
        label="Beskriv anvendelse af Datasæt", 
        widget=forms.Textarea(attrs={
            'rows': 3,
            'cols': 15,
            'required': 'required', 
            'oninvalid': "this.setCustomValidity('Dette felt skal udfyldes.')", 
            'oninput': "this.setCustomValidity('')"
        })
    )
    dataset = forms.ModelChoiceField(queryset=Dataset.objects.all())

    class Meta:
        model = UserDataset  # Use the UserDataset model
        fields = ['dataset', 'description']



