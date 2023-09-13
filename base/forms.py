from django import forms
from base.models import Course,Course_content , Category
import datetime

class BootstrapTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control'})
        super(BootstrapTextInput, self).__init__(*args, **kwargs)

class BootstrapNumberInput(forms.NumberInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control'})
        super(BootstrapNumberInput, self).__init__(*args, **kwargs)

class BootstrapDateInput(forms.DateTimeInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control'})
        super(BootstrapDateInput, self).__init__(*args, **kwargs)

class BootstrapSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control'})
        super(BootstrapSelect, self).__init__(*args, **kwargs)

class BootstrapTextarea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control'})
        super(BootstrapTextarea, self).__init__(*args, **kwargs)
        
class BootstrapTimeInput(forms.TimeInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control'})
        super(BootstrapTimeInput, self).__init__(*args, **kwargs)

class BootstrapFileInput(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control-file'})
        super(BootstrapFileInput, self).__init__(*args, **kwargs)

class BootstrapDateInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'form-control', 'type': 'date'})
        super(BootstrapDateInput, self).__init__(*args, **kwargs)

class CourseForm(forms.ModelForm):
    name = forms.CharField(widget=BootstrapTextInput)
    price = forms.DecimalField(widget=BootstrapNumberInput)
    
    # Automatically generate the current date
    course_post_date = forms.DateField(
        widget=BootstrapDateInput(attrs={'readonly': 'readonly'}),
        initial=datetime.date.today()    
        )
    
    # Generate options from the Category model
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=BootstrapSelect
    )
    
    body = forms.CharField(widget=BootstrapTextarea)
    duration = forms.CharField(widget=BootstrapTextInput)
    class Meta:
        model = Course
        fields = ('name', 'price', 'course_post_date', 'category', 'body', 'duration')

# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ('name', 'price', 'course_post_date', 'category', 'body', 'duration')

# class CourseContentForm(forms.ModelForm):

class CourseContentForm(forms.ModelForm):
    content = forms.FileField(
        widget=BootstrapFileInput(attrs={'accept': 'video/*'})
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Course_content
        fields = ['content', 'name', 'body']