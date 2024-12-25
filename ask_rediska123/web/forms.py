from .models import *
from django import forms

# Форма авторизации
class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean_username(self):
        return self.cleaned_data["username"].lower().strip()

# Форма регистрации
class RegistrationForm(forms.ModelForm):
    avatar = forms.ImageField(label="Avatar", required=False)
    repeat_password = forms.CharField(label="Repeat password", widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["repeat_password"]:
            raise forms.ValidationError("Sorry, passwords don't match!")
        if User.objects.filter(email=cleaned_data["email"]).exists():
            raise forms.ValidationError("Sorry, this email address already registered!")
        if User.objects.filter(username=cleaned_data["username"]).exists():
            raise forms.ValidationError("Sorry, this username already registered!")
        return cleaned_data
    
    def save(self):
        # Устанавливаем commit в false показывая что пока не заносим в базу 
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        user.save()
        
        if "avatar" in self.cleaned_data and self.cleaned_data["avatar"]:
            profile = profile.objects.create(user=user)
            profile.avatar = self.cleaned_data["avatar"]
            profile.save()
            
        return user
    
    class Meta:
        model = User
        fields = ("username", "password", "email")


# Форма настройки профиля
class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False) # поле аватара не обязательное
    
    def clean(self):
        cleaned_data = super().clean()
        
        if self.instance.email != cleaned_data["email"] and User.objects.filter(email=cleaned_data["email"]).exists():
            self.add_error("email", "Sorry, this email address already registered!")
        if self.instance.username != cleaned_data["username"] and User.objects.filter(username=cleaned_data["username"].exists()):
            self.add_error("username", "Sorry, this username already registered")
        return cleaned_data 
        
    def save(self):
        user = super().save()
        
        if "avatar" in self.cleaned_data and self.cleaned_data["avatar"]:
            author, created_flag = profile.objects.get_or_create(user=user)
            author.avatar = self.cleaned_data["avatar"]
            author.save()
            
        return user
        
    class Meta:
        model = User
        fields = ("username", "email")

# Форма нового вопроса
class QuestionForm(forms.ModelForm):
    tags = forms.CharField(label="Tags", max_length=128)
    
    def clean(self):
        # Преобразуем строку с тегами через "," в массив
        tags = self.cleaned_data["tags"].split(",")
        # Очищаем теги от пробелов в начале и в конце
        self.cleaned_data["tags"] = [i.strip() for i in tags if i.strip()]
        return self.cleaned_data

    def save(self, author):
        title = self.cleaned_data["title"]
        text = self.cleaned_data["text"]
        tags = self.cleaned_data["tags"]
        #print("TAGS:", tags)

        for i in range(len(tags)):
            if tag.objects.filter(name=tags[i]).exists():
                tags[i] = tag.objects.filter(name=tags[i]).first()
            else:
                tags[i] = tag.objects.create(name=tags[i])
        
        new_question = question(
            title=title,
            text=text,
            author=author,
        )
        
        # нужно сохранить запись чтобы связать с тегами (м-м)
        new_question.save() 
        
        new_question.tags.set(tags)

        return new_question
    
    class Meta:
        model = question
        fields = ("title", "text", "tags")

# Форма ответа на вопрос
class AnswerForm(forms.ModelForm):
    def save(self, author, answered_question):
        text = self.cleaned_data["text"]
        
        new_answer = answer(
            text = text,
            author = author,
            answered_question = answered_question,
        )
        
        new_answer.save()
        
        return new_answer
        
    class Meta:
        model = answer
        fields = ("text",)

        