import hashlib
from django.db import models
from django import forms

class Genres(models.Model):
    name = models.CharField(max_length = 250)

class Login(models.Model):
    email = models.EmailField(max_length = 255, unique=True)
    password = models.CharField(max_length = 255, default = None)

    def __unicode__(self):
        return self.email

    def create_hash(self):
        m = hashlib.md5()
        m.update(self.password)
        return m.hexdigest()

    def save(self, *args, **kwargs):
        if self.password is not None:
            self.password = self.create_hash()
        super(Login, self).save(*args, **kwargs)

class Shows(models.Model):
    name = models.CharField(max_length = 255)
    poster = models.CharField(max_length = 255)
    summary = models.TextField()

class Users(models.Model):
    login = models.ForeignKey('Login')
    name = models.CharField(max_length = 255)
    profile_pic = models.CharField(max_length = 255)

class Rating_show(models.Model):
    show = models.ForeignKey('Shows')
    user = models.ForeignKey('Users')
    rating  = models.DecimalField(max_digits = 5, decimal_places=2)

class Review_show(models.Model):
    user = models.ForeignKey('Users')
    show = models.ForeignKey('Shows')
    review = models.TextField()
    
class Shows_genres(models.Model):
    show = models.ForeignKey('Shows')
    genre = models.ForeignKey('Genres')

class RegistrationForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Login
        fields = ['name', 'email', 'password']

class ProfilePic(models.Model):
    profpic = models.FileField(upload_to="images/")

class ProfilePicForm(forms.Form):
    profpic = forms.FileField(
        label='Select an image file',
        )
