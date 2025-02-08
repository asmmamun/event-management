from django import forms
from events.models import Category, Event, Participant

class CategoryForm(forms.ModelForm):  
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'rows': 4, 'placeholder': 'Enter category description'}),
        }

class EventForm(forms.ModelForm):  
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Enter event name'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'rows': 4, 'placeholder': 'Enter event description'}),
            'date': forms.DateInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Enter event location'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
        }



class ParticipantForm(forms.ModelForm):
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class':'w-15 h-3 text-blue-500 border-gray-300 focus:ring focus:ring-blue-300 inline-block'
        }),
        required=True
    )

    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500',
                'placeholder': "Enter participant's name"
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500',
                'placeholder': "Enter participant's email"
            })
        }


