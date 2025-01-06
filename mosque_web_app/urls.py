"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('mosque_web_admin/', views.mosque_web_admin_view, name='mosque_web_admin'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('about_admin/', views.about_admin, name='about_admin'),
    path('activity/', views.activity, name='activity'),
    path('activities_admin/', views.activities_admin, name='activities_admin'),
    path('event/', views.event, name='event'),
    path('events_admin/', views.events_admin, name='events_admin'),
    path('sermon/', views.sermon, name='sermon'),
    path('sermons_admin/', views.sermons_admin, name='sermons_admin'),
    path('blog/', views.blog, name='blog'),
    path('blogs_admin/', views.blogs_admin, name='blogs_admin'),
    path('team/', views.team, name='team'),
    path('team_admin/', views.team_admin, name='team_admin'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('testimonial_admin/', views.testimonial_admin, name='testimonial_admin'),
    path('404/', views.view_404, name='404'),
    path('view_404_admin/', views.view_404_admin, name='view_404_admin'),
    path('set_cookie_consent/', views.set_cookie_consent, name='set_cookie_consent'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('list_view_404_admin_view/', views.list_view_404_admin_view, name='list_view_404_admin_view'),
    path('actualizar_view_404_admin/<id_view_404_admin>', views.actualizar_view_404_admin, name='actualizar_view_404_admin'),
    path('eliminar_view_404_admin/<id_view_404_admin>', views.eliminar_view_404_admin, name='eliminar_view_404_admin'),
    path('list_testimonial_admin_view/', views.list_testimonial_admin_view, name='list_testimonial_admin_view'),
    path('actualizar_testimonial_admin/<id_testimonial_admin>', views.actualizar_testimonial_admin, name='actualizar_testimonial_admin'),
    path('eliminar_testimonial_admin/<id_testimonial_admin>', views.eliminar_testimonial_admin, name='eliminar_testimonial_admin'),
    path('list_team_admin_view/', views.list_team_admin_view, name='list_team_admin_view'),
    path('actualizar_team_admin/<id_team_admin>', views.actualizar_team_admin, name='actualizar_team_admin'),
    path('eliminar_team_admin/<id_team_admin>', views.eliminar_team_admin, name='eliminar_team_admin'),
    path('list_blogs_admin_view/', views.list_blogs_admin_view, name='list_blogs_admin_view'),
    path('actualizar_blogs_admin/<id_blogs_admin>', views.actualizar_blogs_admin, name='actualizar_blogs_admin'),
    path('eliminar_blogs_admin/<id_blogs_admin>', views.eliminar_blogs_admin, name='eliminar_blogs_admin'),
    path('list_sermons_admin_view/', views.list_sermons_admin_view, name='list_sermons_admin_view'),
    path('actualizar_sermons_admin/<id_sermons_admin>', views.actualizar_sermons_admin, name='actualizar_sermons_admin'),
    path('eliminar_sermons_admin/<id_sermons_admin>', views.eliminar_sermons_admin, name='eliminar_sermons_admin'),
    path('list_events_admin_view/', views.list_events_admin_view, name='list_events_admin_view'),
    path('actualizar_events_admin/<id_events_admin>', views.actualizar_events_admin, name='actualizar_events_admin'),
    path('eliminar_events_admin/<id_events_admin>', views.eliminar_events_admin, name='eliminar_events_admin'),
    path('list_activities_admin_view/', views.list_activities_admin_view, name='list_activities_admin_view'),
    path('actualizar_activities_admin/<id_activities_admin>', views.actualizar_activities_admin, name='actualizar_activities_admin'),
    path('eliminar_activities_admin/<id_activities_admin>', views.eliminar_activities_admin, name='eliminar_activities_admin'),
    path('list_about_admin_view/', views.list_about_admin_view, name='list_about_admin_view'),
    path('actualizar_about_admin/<id_about_admin>', views.actualizar_about_admin, name='actualizar_about_admin'),
    path('eliminar_about_admin/<id_about_admin>', views.eliminar_about_admin, name='eliminar_about_admin'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('list_contact_view/', views.list_contact_view, name='list_contact_view'),
    path('actualizar_contact/<id_contact>', views.actualizar_contact, name='actualizar_contact'),
    path('eliminar_contact/<id_contact>', views.eliminar_contact, name='eliminar_contact'),



]
