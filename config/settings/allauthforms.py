from allauth.account.forms import LoginForm

class PhoneNumberLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = "Phone Number"