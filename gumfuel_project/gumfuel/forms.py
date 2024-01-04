from django import forms
from .models import Comment, Exercise, Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


# форма для входа-------------------------------------------------------------------------------------------------------

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Логин'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))


# форма для регистрации ------------------------------------------------------------------------------------------------

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Логин'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя...'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша фамилия...'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


# Форма для комментариев------------------------------------------------------------------------------------------------


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }


# Форма для добовления постов-------------------------------------------------------------------------------------------

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('title', 'content', 'content_full', 'photo1', 'photo2', 'photo3', 'category')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назваине упражнения'
            }),

            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание упражнения'
            }),

            'content_full': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Полное описание упражнения'
            }),

            'photo1': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'photo2': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'photo3': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Категория упрожнения'
            })
        }


# Форма для изменения акка----------------------------------------------------------------------------------------------
class EditAccountForm(UserChangeForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Логин'
    }))

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя...'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша фамилия...'
    }))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта'
    }))

    old_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Текущий пароль'
    }))

    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Новый пароль'
    }))

    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'old_password', 'new_password', 'confirm_password')


# изменение профиля
class EditProfileForm(forms.ModelForm):
    photo = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Телефон'
    }))

    about_me = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Осебе'
    }))

    class Meta:
        model = Profile
        fields = ('photo', 'phone_number', 'about_me')





















