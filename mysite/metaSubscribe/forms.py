from django import forms

class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email Address")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@sdfi.dk'):
            raise forms.ValidationError("Email must end with '@sdfi.dk'")
        return email
