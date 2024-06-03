from allauth.account.forms import SignupForm, LoginForm


# Override allauth forms [https://stackoverflow.com/questions/23580771/overwrite-django-allauth-form-field]
class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'aria-describedby': 'hint_id_password1'
        })


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({
            'aria-describedby': 'hint_id_password'
        })
