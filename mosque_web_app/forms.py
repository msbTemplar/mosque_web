# forms.py
from django import forms
from .models import ContactMessage, About, Activity, Event, Error404, Sermon, Blog, TeamMember, Testimonial, Newsletter, AboutImages, Footer, Donation, Post, Page, ContactInfo, BestVideos, Tab, TabPage
import json
from django.core.exceptions import ValidationError

from django import forms
from .models import Testimonial
import json
from django.utils.text import slugify
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

""" class CustomUserCreationForm1(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Introduce una dirección de correo válida.")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        return email """
        
class TabPageForm(forms.ModelForm):
    class Meta:
        model = TabPage
        fields = [
            'tab_page_name',
            'tab_page_url_name',
            'tab_img_url',
            'tab_file',
            'tab_date_page',
            'tab_time_page',
            'tab_day_page',
            'is_active',
        ]
        widgets = {
            'tab_page_name': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Nombre de la Página del Tab',
                'style': 'height: 55px;',
            }),
            'tab_page_url_name': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'URL de la Página del Tab',
                'style': 'height: 55px;',
            }),
            'tab_img_url': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'tab_file': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'tab_date_page': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Fecha de la Página del Tab',
                'type': 'date',
            }),
            'tab_time_page': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Hora de la Página del Tab',
                'type': 'time',
            }),
            'tab_day_page': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-top: 10px;',
            }),
        }
        
class TabForm(forms.ModelForm):
    class Meta:
        model = Tab
        fields = [
            'tab_nombre',
            'tab_slug',
            'tab_description',
            'tab_url',
            'tab_img_url',
            'tab_file',
            'tab_date_page',
            'tab_time_page',
            'tab_day_page',
            'is_active'
        ]
        widgets = {
            'tab_nombre': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Ingrese el nombre',
                'style': 'height: 55px;',
            }),
            'tab_slug': forms.TextInput(attrs={  # Agregar input para el slug
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Slug automático basado en el nombre',
                'style': 'height: 55px;',
            }),
            'tab_description': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Ingrese la descripción',
                'style': 'height: 150px;',
            }),
            'tab_url': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Ingrese la URL',
                'style': 'height: 55px;',
            }),
            'tab_img_url': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'tab_file': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'tab_date_page': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Fecha de BestVideos',
                'type': 'date',
            }),
            'tab_time_page': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Hora de BestVideos',
                'type': 'time',
            }),
            'tab_day_page': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-top: 10px;',
            }),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Si el slug está vacío, lo genera automáticamente
        if not instance.tab_slug:
            instance.tab_slug = slugify(instance.tab_nombre)
        
        if commit:
            instance.save()
        return instance


class BestVideosForm(forms.ModelForm):
    class Meta:
        model = BestVideos
        fields = [
            'best_video_ref',
            'best_video_name',
            'best_video_description',
            'best_video_url',
            'best_video_img_url',
            'best_video_file',
            'date_page',
            'time_page',
            'day_page',
            'is_active',
        ]
        widgets = {
            'best_video_ref': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Referencia del Video',
                'style': 'height: 55px;',
            }),
            'best_video_name': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Nombre del Video',
                'style': 'height: 55px;',
            }),
            'best_video_description': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Descripción del Video',
                'style': 'height: 150px;',
            }),
            'best_video_url': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Best videos URL',
                'style': 'height: 55px;',
            }),
            'best_video_img_url': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'best_video_file': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'date_page': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Fecha del Video',
                'type': 'date',
            }),
            'time_page': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Hora del Video',
                'type': 'time',
            }),
            'day_page': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-top: 10px;',
            }),
        }

    

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text="Requerido. Introduce una dirección de correo válida.",
        widget=forms.EmailInput(attrs={
            'class': 'form-control border-1 bg-light px-4',
            'placeholder': 'Correo Electrónico',
            'style': 'height: 55px;'
        })
    )
    username = forms.CharField(
        required=True,
        help_text="El nombre de usuario debe tener entre 4 y 150 caracteres. No use caracteres especiales.",
        widget=forms.TextInput(attrs={
            'class': 'form-control border-1 bg-light px-4',
            'placeholder': 'Nombre de Usuario',
            'style': 'height: 55px;'
        })
    )
    password1 = forms.CharField(
        required=True,
        help_text="La contraseña debe tener al menos 8 caracteres y contener al menos un número, una mayúscula y un carácter especial.",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-1 bg-light px-4',
            'placeholder': 'Contraseña',
            'style': 'height: 55px;'
        })
    )
    password2 = forms.CharField(
        required=True,
        help_text="Introduzca nuevamente la contraseña para confirmarla.",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-1 bg-light px-4',
            'placeholder': 'Confirmar Contraseña',
            'style': 'height: 55px;'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        return email




class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = [
            'phone_number',
            'email',
            'facebook_url',
            'twitter_url',
            'linkedin_url',
            'instagram_url',
            'date_contact_info',
            'time_contact_info',
            'day_contact_info',
            'img_url_contact_info',
            'file_contact_info',
            'is_active',
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Número de Teléfono',
                'style': 'height: 55px;',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Correo Electrónico',
                'style': 'height: 55px;',
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'URL de Facebook',
                'style': 'height: 55px;',
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'URL de Twitter',
                'style': 'height: 55px;',
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'URL de LinkedIn',
                'style': 'height: 55px;',
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'URL de Instagram',
                'style': 'height: 55px;',
            }),
            'date_contact_info': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Fecha',
                'type': 'date',
                'style': 'height: 55px;',
            }),
            'time_contact_info': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Hora',
                'type': 'time',
                'style': 'height: 55px;',
            }),
            'day_contact_info': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'img_url_contact_info': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'file_contact_info': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 10px;',
            }),
        }


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'title',
            'url_name',
            'is_dropdown',
            'parent',
            'welcome_to_the_mosque',
            'purity_comes_from_faith',
            'date_page',
            'time_page',
            'day_page',
            'img_url_page',
            'file_page',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Título de la Página',
                'style': 'height: 55px;',
            }),
            'url_name': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Nombre de la URL',
                'style': 'height: 55px;',
            }),
            'is_dropdown': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 10px;',
            }),
            'parent': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'welcome_to_the_mosque': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Bienvenida a la Mezquita',
                'style': 'height: 55px;',
            }),
            'purity_comes_from_faith': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'La pureza proviene de la fe',
                'style': 'height: 150px;',
            }),
            'date_page': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Fecha',
                'type': 'date',
                'style': 'height: 55px;',
            }),
            'time_page': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Hora',
                'type': 'time',
                'style': 'height: 55px;',
            }),
            'day_page': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'img_url_page': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'file_page': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 10px;',
            }),
        }



class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'title',
            'description',
            'amount_required',
            'amount_collected',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Título de la Donación',
                'style': 'height: 55px;',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Descripción de la Donación',
                'style': 'height: 150px;',
            }),
            'amount_required': forms.NumberInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Monto Total Requerido',
                'style': 'height: 55px;',
            }),
            'amount_collected': forms.NumberInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Monto Recaudado',
                'style': 'height: 55px;',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 10px;',
            }),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title_post',
            'description_post',
            'link_post',
            'explore_link_latest_post_date_footer',
            'explore_link_latest_post_time_footer',
            'explore_link_latest_post_day_footer',
            'image_post',
            'file_post',
        ]
        widgets = {
            'title_post': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Título del Post',
                'style': 'height: 55px;',
            }),
            'description_post': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Descripción del Post',
                'style': 'height: 150px;',
            }),
            'link_post': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Enlace al Post',
                'style': 'height: 55px;',
            }),
            'explore_link_latest_post_date_footer': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Fecha de Publicación',
                'type': 'date',
            }),
            'explore_link_latest_post_time_footer': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Hora de Publicación',
                'type': 'time',
            }),
            'explore_link_latest_post_day_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'image_post': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'file_post': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
        }

class FooterForm(forms.ModelForm):
    class Meta:
        model = Footer
        fields = [
            'subscribe_footer',
            'description_subscribe_footer',
            'subscibe_boton_footer',
            'themosque_footer',
            'themosque_description_footer',
            'our_mosque_footer',
            'our_address_footer',
            'our_address_address_footer',
            'our_mobile_footer',
            'our_mobile_mobile_footer',
            'explore_link_footer',
            'explore_link_home_footer',  # Relación ForeignKey
            'explore_link_about_footer',  # Relación ForeignKey
            'explore_link_features_footer',  # Relación ForeignKey
            'explore_link_contact_footer',  # Relación ForeignKey
            'explore_link_blog_footer',  # Relación ForeignKey
            'explore_link_events_footer',  # Relación ForeignKey
            'explore_link_donations_footer',  # Relación ForeignKey
            'explore_link_sermons_footer',  # Relación ForeignKey
            'explore_link_latest_post_footer',
            'explore_link_posts_footer',  # Relación ForeignKey
            'date_footer',
            'time_footer',
            'day_footer',
            'description_footer',
            'title_footer',
            'link_footer',
            'img_url_footer',
            'file_footer',
            'site_name_footer',
            'is_active',
        ]
        widgets = {
            'subscribe_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Subscribe Footer',
                'style': 'height: 55px;',
            }),
            'description_subscribe_footer': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description Subscribe Footer',
                'style': 'height: 200px;',
            }),
            'subscibe_boton_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Subscribe Button Footer',
                'style': 'height: 55px;',
            }),
            'themosque_footer': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'The Mosque Footer',
                'style': 'height: 100px;',
            }),
            'themosque_description_footer': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'The Mosque Description Footer',
                'style': 'height: 100px;',
            }),
            'our_mosque_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Our Mosque Footer',
                'style': 'height: 55px;',
            }),
            'our_address_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Our Address Footer',
                'style': 'height: 55px;',
            }),
            'our_address_address_footer': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Our Address Details Footer',
                'style': 'height: 100px;',
            }),
            'our_mobile_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Our Mobile Footer',
                'style': 'height: 55px;',
            }),
            'our_mobile_mobile_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Our Mobile Details Footer',
                'style': 'height: 55px;',
            }),
            'explore_link_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Explore Link Footer',
                'style': 'height: 55px;',
            }),
            'explore_link_home_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Explore Link Home Footer',
                'style': 'height: 55px;',
            }),
            'explore_link_about_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'explore_link_features_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'explore_link_contact_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'explore_link_blog_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'explore_link_events_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'explore_link_donations_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'explore_link_sermons_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'explore_link_posts_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'explore_link_latest_post_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Footer Title',
                'style': 'height: 55px;',
            }),
            'date_footer': forms.DateInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Footer Date',
                'type': 'date',
            }),
            'time_footer': forms.TimeInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Footer Time',
                'type': 'time',
            }),
            'day_footer': forms.Select(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'description_footer': forms.Textarea(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Description Footer',
                'style': 'height: 200px;',
            }),
            'title_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Footer Title',
                'style': 'height: 55px;',
            }),
            'link_footer': forms.URLInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Footer Link',
                'style': 'height: 55px;',
            }),
            'img_url_footer': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'file_footer': forms.ClearableFileInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'style': 'height: 55px;',
            }),
            'site_name_footer': forms.TextInput(attrs={
                'class': 'form-control border-1 bg-light px-4',
                'placeholder': 'Site Name',
                'style': 'height: 55px;',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 10px;',
            }),
        }




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