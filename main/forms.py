from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Room



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]     

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # user = authenticate(username=username, password=password)
        # if not user or not user.is_active:
        #     raise forms.ValidationError("Invalid credentials")
        return self.cleaned_data
    
class UserForm(forms.ModelForm):

    class Meta:
        model = User 
        fields = ['username','password','email']

    def clean(self):
        super(UserForm, self).clean()
        username = self.cleaned_data.get('username')
        if username.isnumeric():
            self._errors['username'] = self.error_class(['username cannot be numbers'])
        if len(username) < 5:
            self._errors['username'] = self.error_class(['username must be more than 5 characters'])

        return self.cleaned_data    
