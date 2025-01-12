# forms.py
from django import forms
from .models import ContactMessage, About, Activity, Event, Error404, Sermon, Blog, TeamMember, Testimonial, Newsletter, AboutImages
import json
from django.core.exceptions import ValidationError

from django import forms
from .models import Testimonial
import json

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']  # Solo necesitamos el correo electrónico
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-white p-3',
                'placeholder': 'Your Email',
                'style': 'height: 55px;'
            }),
        }
        labels = {
            'email': ''
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = [
            'testimonial_full_name',
            'testimonial_position',
            'testimonial_status',
            'testimonial_description',
            'testimonial_date_of_birth',
            'testimonial_email',
            'testimonial_phone_number',
            'testimonial_link',
            'testimonial_img_url',
            'testimonial_date',
            'testimonial_time',
            'testimonial_day',
            'testimonial_social_links',
        ]
        widgets = {
            'testimonial_full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
            }),
            'testimonial_position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter position',
            }),
            'testimonial_status': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter status',
            }),
            'testimonial_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description',
                'rows': 4,
            }),
            'testimonial_date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'testimonial_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
            }),
            'testimonial_phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),
            'testimonial_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter link (optional)',
            }),
            'testimonial_img_url': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'testimonial_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'testimonial_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'testimonial_day': forms.Select(attrs={
                'class': 'form-control',
            }),
            'testimonial_social_links': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '{"LinkedIn": "https://linkedin.com/in/example", "Twitter": "https://twitter.com/example"}',
                'rows': 7,
            }),
        }

    def clean_testimonial_social_links(self):
        data = self.cleaned_data.get('testimonial_social_links')
        if data:
            try:
                if isinstance(data, str):
                    json_data = json.loads(data)
                elif isinstance(data, dict):
                    json_data = data
                else:
                    raise forms.ValidationError("Invalid format for social links.")
            except json.JSONDecodeError:
                raise forms.ValidationError("Invalid JSON format for social links.")
            return json.dumps(json_data)  # Convertir a string JSON
        return data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer el valor inicial si el campo está vacío
        if not self.initial.get('testimonial_social_links'):
            self.initial['testimonial_social_links'] = '{"LinkedIn": "https://linkedin.com/in/example", "Twitter": "https://twitter.com/example"}'


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = [
            'team_full_name',
            'team_position',
            'team_status',
            'team_life_situation',
            'team_description',
            'team_date_of_birth',
            'team_email',
            'team_address',
            'team_phone_number',
            'team_link',
            'team_img_url',
            'team_date_start',
            'team_time_start',
            'team_day_start',
            'team_social_links',
        ]
        widgets = {
            'team_full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
            }),
            'team_position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Position',
            }),
            'team_status': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Status',
            }),
            'team_life_situation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Life Situation',
            }),
            'team_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description',
            }),
            'team_date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'team_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),
            'team_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Address',
            }),
            'team_phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
            }),
            'team_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link (optional)',
            }),
            'team_img_url': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'team_date_start': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'team_time_start': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'team_day_start': forms.Select(attrs={
                'class': 'form-control',
            }),
            'team_social_links': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '{"LinkedIn": "https://linkedin.com/in/example", "Twitter": "https://twitter.com/example"}',
            }),
        }
    def clean_team_social_links(self):
        data = self.cleaned_data.get('team_social_links')
        if data:
            try:
                if isinstance(data, str):
                    json_data = json.loads(data)
                elif isinstance(data, dict):
                    json_data = data
                else:
                    raise ValidationError("Invalid format for social links.")
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON format.")
            return json.dumps(json_data)  # Devolver como string JSON para almacenamiento
        return data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer el valor inicial si el campo está vacío
        if not self.initial.get('team_social_links'):
            self.initial['team_social_links'] = '{"LinkedIn": "https://linkedin.com/in/example", "Twitter": "https://twitter.com/example"}'




class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'blog_title',
            'description_blog',
            'link_blog',
            'img_url_blog',
            'date_blog',
            'time_blog',
            'day_blog',
            'number_coments_blog',
        ]
        widgets = {
            'blog_title': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Blog Title',
                'style': 'height: 55px;',
            }),
            'description_blog': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Blog Description',
                'style': 'height: 200px;',
            }),
            'link_blog': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Blog Link (optional)',
                'style': 'height: 55px;',
            }),
            'img_url_blog': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'date_blog': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Blog Date',
                'type': 'date',
            }),
            'time_blog': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Blog Time',
                'type': 'time',
            }),
            'day_blog': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'number_coments_blog': forms.NumberInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Number of Comments',
                'style': 'height: 55px;',
            }),
        }


class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        fields = ['sermon_title', 'description_sermon', 'link_sermon', 'img_url_sermon', 'date_sermon', 'time_sermon', 'day_sermon', 'file_sermon']
        widgets = {
            'sermon_title': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Sermon Title',
                'style': 'height: 55px;',
            }),
            'description_sermon': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Sermon Description',
                'style': 'height: 200px;',
            }),
            'link_sermon': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Sermon Link',
                'style': 'height: 55px;',
            }),
            'img_url_sermon': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'date_sermon': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Sermon Date',
                'type': 'date',
            }),
            'time_sermon': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Sermon Time',
                'type': 'time',
            }),
            'day_sermon': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'file_sermon': forms.ClearableFileInput(attrs={  # Nuevo widget para file_sermon
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
        }


class Error404Form(forms.ModelForm):
    class Meta:
        model = Error404
        fields = ['error', 'error_title', 'error_description']
        widgets = {
            'error': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Error Code (e.g., 404)',
                'style': 'height: 55px;',
            }),
            'error_title': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Error Title',
                'style': 'height: 55px;',
            }),
            'error_description': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Error Description',
                'style': 'height: 200px;',
            }),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title_event', 'description_title_event', 'link_event', 'img_url_event', 'date_event', 'time_event', 'day_event', 'file_event']
        widgets = {
            'title_event': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Event Title',
                'style': 'height: 55px;',
            }),
            'description_title_event': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Event Description',
                'style': 'height: 200px;',
            }),
            'link_event': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Event Link',
                'style': 'height: 55px;',
            }),
            'img_url_event': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'date_event': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Event Date',
                'type': 'date',
            }),
            'time_event': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Event Time',
                'type': 'time',
            }),
            'day_event': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'file_event': forms.ClearableFileInput(attrs={  # Nuevo widget para file_sermon
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'activity_title',
            'activity_mosque_development',
            'description_activity_mosque_development',
            'activity_charity_donation',
            'description_activity_charity_donation',
            'activity_quran_learning',
            'description_activity_quran_learning',
            'activity_hadith_sunnah',
            'description_activity_hadith_sunnah',
            'activity_parent_education',
            'description_activity_parent_education',
            'activity_help_orphans',
            'description_activity_help_orphans',
            'activity_testimonial',
            'activity_title_testimonial',
        ]
        widgets = {
            'activity_title': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Activity Title',
                'style': 'height: 55px;',
            }),
            'activity_mosque_development': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Mosque Development Activity',
                'style': 'height: 55px;',
            }),
            'description_activity_mosque_development': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description of Mosque Development Activity',
                'style': 'height: 200px;',
            }),
            'activity_charity_donation': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Charity and Donation Activity',
                'style': 'height: 55px;',
            }),
            'description_activity_charity_donation': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description of Charity and Donation Activity',
                'style': 'height: 200px;',
            }),
            'activity_quran_learning': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Quran Learning Activity',
                'style': 'height: 55px;',
            }),
            'description_activity_quran_learning': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description of Quran Learning Activity',
                'style': 'height: 200px;',
            }),
            'activity_hadith_sunnah': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Hadith and Sunnah Activity',
                'style': 'height: 55px;',
            }),
            'description_activity_hadith_sunnah': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description of Hadith and Sunnah Activity',
                'style': 'height: 200px;',
            }),
            'activity_parent_education': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Parent Education Activity',
                'style': 'height: 55px;',
            }),
            'description_activity_parent_education': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description of Parent Education Activity',
                'style': 'height: 200px;',
            }),
            'activity_help_orphans': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Help Orphans Activity',
                'style': 'height: 55px;',
            }),
            'description_activity_help_orphans': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description of Help Orphans Activity',
                'style': 'height: 200px;',
            }),
            'activity_testimonial': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Activity Testimonial',
                'style': 'height: 55px;',
            }),
            'activity_title_testimonial': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Activity Title Testimonial',
                'style': 'height: 55px;',
            }),
        }



class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = [
            'about_the_mosque',
            'allah_helps_those',
            'description_about',
            'our_vision',
            'description_our_vision',
            'our_mission',
            'description_our_mission',
            'raised',
            'raised_value',
            'description_raised',
            'img_url_raised_about',
            'charity_and_donation',
            'parent_education',
            'hadith_and_sunnah',
            'mosque_development',
            'file_about',
        ]
        widgets = {
            'about_the_mosque': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'About the Mosque',
                'style': 'height: 55px;',
            }),
            'allah_helps_those': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Allah Helps Those',
                'style': 'height: 55px;',
            }),
            'description_about': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description About the Mosque',
                'style': 'height: 200px;',
            }),
            'our_vision': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Our Vision',
                'style': 'height: 55px;',
            }),
            'description_our_vision': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description of Our Vision',
                'style': 'height: 200px;',
            }),
            'our_mission': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Our Mission',
                'style': 'height: 55px;',
            }),
            'description_our_mission': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description of Our Mission',
                'style': 'height: 200px;',
            }),
            'raised': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Raised',
                'style': 'height: 55px;',
            }),
            'raised_value': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Raised Value',
                'style': 'height: 55px;',
            }),
            'description_raised': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description of Raised Funds',
                'style': 'height: 200px;',
            }),
            'img_url_raised_about': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'charity_and_donation': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Charity and Donation',
                'style': 'height: 55px;',
            }),
            'parent_education': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Parent Education',
                'style': 'height: 55px;',
            }),
            'hadith_and_sunnah': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Hadith and Sunnah',
                'style': 'height: 55px;',
            }),
            'mosque_development': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Mosque Development',
                'style': 'height: 55px;',
            }),
            'file_about': forms.ClearableFileInput(attrs={  # Nuevo widget para file_sermon
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
        }

class AboutImagesForm(forms.ModelForm):
    class Meta:
        model = AboutImages
        fields = [
            'about_images_the_about_image',
            'img_url_about_images',
        ]
        widgets = {
            'about_images_the_about_image': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'About the Mosque',
                'style': 'height: 55px;',
            }),
            'img_url_about_images': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
        }

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Your Name',
                'style': 'height: 55px;',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Your Email',
                'style': 'height: 55px;',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Subject',
                'style': 'height: 55px;',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Your Message',
                'style': 'height: 200px;',
            }),
        }