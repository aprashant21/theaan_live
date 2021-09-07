from django import forms
from django.forms import widgets
from .models import API, BLOG, NOTE




class APIForm(forms.ModelForm):
    class Meta:
        model = API
        fields = ('apiName','apiLink')
        widgets= {
            'apiName': forms.TextInput(attrs={'class':'form-control'}),
            'apiLink': forms.TextInput(attrs={'class':'form-control'})
        }

class BLOGForm(forms.ModelForm):
    class Meta:
        model = BLOG
        fields = ('blogTitle','blogCategory','blogImage','blogDate','blogSummary','blogDesc')
        widgets= {
            'blogTitle': forms.TextInput(attrs={'class':'form-control'}),
            'blogCategory': forms.Select(attrs={'class':'form-control'}),
            'blogImage': forms.FileInput(attrs={'class':'form-control'}),
            'blogDate': forms.DateInput(attrs={'type': 'date'}),
            'blogSummary':forms.Textarea(attrs={'class':'form-control ','rows':2}),
            'blogDesc': forms.Textarea(attrs={'class':'form-control','rows':8})
            }

class NOTEForm(forms.ModelForm):
    class Meta:
        model = NOTE
        fields = ('noteTitle','noteDate','noteDesc')
        widgets= {
            'noteTitle': forms.TextInput(attrs={'class':'form-control'}),
            'noteDate': forms.DateInput(attrs={'type': 'date'}),
            'noteDesc': forms.Textarea(attrs={'class':'form-control', 'row':'8','type':'TextArea'})
            }