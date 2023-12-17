from django import forms
from .models import Dataset
from .models import CustomUser
from .models import UserDataset



class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")

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
    dataset = forms.ModelChoiceField(queryset=Dataset.objects.none())  # Initialize with no queryset

    class Meta:
        model = UserDataset
        fields = ['dataset', 'description']

    def __init__(self, *args, **kwargs):
        exclude_datasets = kwargs.pop('exclude_datasets', None)
        super(RegisterDatasetForm, self).__init__(*args, **kwargs)
        if exclude_datasets is not None:
            self.fields['dataset'].queryset = Dataset.objects.exclude(id__in=exclude_datasets).order_by('TITEL')
        else:
            self.fields['dataset'].queryset = Dataset.objects.all().order_by('TITEL')




