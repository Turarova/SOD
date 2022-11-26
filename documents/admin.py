from django.contrib import admin
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import StudentDocument

class StudentDocumentForm(forms.ModelForm):
    class Meta:
        widgets = {                         
            'phone': PhoneNumberPrefixWidget(initial='US'),
        }

@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    form = StudentDocumentForm
