from django.contrib import admin
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Counselor, StudentDocument

class CounselorForm(forms.ModelForm):
    class Meta:
        widgets = {                         
            'phone': PhoneNumberPrefixWidget(initial='US'),
        }

@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    form = CounselorForm

admin.site.register(StudentDocument)

