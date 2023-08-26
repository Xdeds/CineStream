from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, Raiting, RaitingStar

class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    captcha = ReCaptchaField()
    class Meta:
        model = Reviews
        fields = ("name", "email", "text", "captcha")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }

class RaitingForm(forms.ModelForm):
    """Формы добавление рейтинга"""
    star = forms.ModelChoiceField(queryset=RaitingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Raiting
        fields = ("star", )