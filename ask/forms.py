from django import forms
from .models import Question, Profile, Answer
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input inputlogin'}), label=u'Имя пользователя',
                               max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input inputlogin'}), label=u'Пароль',
                               max_length=30)
    redirect = forms.CharField(widget=forms.HiddenInput)


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input inputlogin'}), label=u'Логин', max_length=30)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input inputlogin'}), label='E-mail', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input inputlogin'}), label=u'Пароль', max_length=30)
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input inputlogin'}), label=u'Повторите пароль', max_length=30)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self._errors["username"] = self.error_class([u'Пользователь с таким именем уже существует'])
            del self.cleaned_data["username"]
        return username

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password is None:
            self._errors["password"] = self.error_class([u'Не введен пароль'])
        elif password != repeat_password:
            self._errors["password"] = self.error_class([u'Пароли не совпадают'])
        elif len(password) < 6:
            self._errors["password"] = self.error_class([u'Введите пароль длиной не менее 6 символов'])

        return cleaned_data


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'avatar',
        )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'text': forms.Textarea(attrs={'class': 'input'})
        }
        labels = {
            'title': u'Название',
            'text': u'Текст вопроса'
        }

    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), label=u'Теги', required=False)

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(QuestionForm, self).__init__(*args,  **kwargs)

    def save(self, commit=True):
        obj = super(QuestionForm, self).save(commit=False)
        obj.author = self.author.user
        if commit:
            obj.save()
        return obj


class PictureForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['picture']



class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'input'}))

    def save(self, q, user):
        answer = Answer(text=self.cleaned_data['text'], author=user, question=q)
        answer.save()
        return answer