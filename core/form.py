from cProfile import label

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import University, Group, Profile, Note, Comment


class RegistrationForm(UserCreationForm):
    university = forms.ModelChoiceField(queryset=University.objects.all(), required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "university", "course"]
        labels = {
            "name": "Group Name",
            "university": "University",
            "course": "Course Name"
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        try:
            profile = Profile.objects.get(user=user)
            self.fields['university'].queryset = profile.universities.all()
        except Profile.DoesNotExist:
            self.fields['university'].queryset = University.objects.none()

class JoinUniversityForm(forms.Form):
    university = forms.ModelChoiceField(queryset=University.objects.none(), label="University")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            try:
                profile = Profile.objects.get(user=user)
                self.fields['university'].queryset = University.objects.exclude(id__in=profile.universities.values_list('id', flat=True))
            except Profile.DoesNotExist:
                self.fields['university'].queryset = University.objects.all()
        else:
            self.fields['university'].queryset = University.objects.all()

class GroupNoteCreationForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'context', 'group']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        group_id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)
        if group_id and user:
            try:
                group = Group.objects.get(id=group_id)
                self.fields['group'].queryset = Group.objects.filter(id=group_id)
                self.fields['group'].initial = group
                self.fields['group'].disabled = True
            except Group.DoesNotExist:
                self.fields['group'].queryset = Group.objects.none()

class PersonalNoteCreationForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'context']

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['context']

        labels = {
            'context': 'Comment'
        }
