from django import forms
from .models import Dataset
from .models import CustomUser



class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email Address")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@sdfi.dk'):
            raise forms.ValidationError("Email must end with '@sdfi.dk'")
        return email

class RegisterDatasetForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':15}))
    dataset = forms.ModelChoiceField(queryset=Dataset.objects.all())

    class Meta:
        model = CustomUser.datasets.through  # This is the UserDataset table created implicitly
        fields = ['dataset', 'description']
