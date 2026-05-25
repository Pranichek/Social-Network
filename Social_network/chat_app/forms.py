from django import forms
from .models import Chat
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateGroupChatForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = True
    )
    
    class Meta:
        model = Chat
        fields = ['name', 'avatar', 'users']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введіть назву', 
                'class' : 'form-control'
            })
        }

    def save(self, commit = True):
        chat = super().save(commit = False)
        chat.is_group = True
        
        if commit:
            chat.save()
            
        return chat

class GroupChatUpdateForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )
    
    class Meta:
        model = Chat
        fields = ['name', 'avatar','users']
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'form-control'})
        }

class AddChatMemberForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = True
    )