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
    path('register/', views.register, name='register'),
    
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('mosque_web_admin/', views.mosque_web_admin_view, name='mosque_web_admin'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('about_admin/', views.about_admin, name='about_admin'),
    path('about_images_admin/', views.about_images_admin, name='about_images_admin'),
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
    path('list_about_images_admin_view/', views.list_about_images_admin_view, name='list_about_images_admin_view'),
    path('actualizar_about_images_admin/<id_about_images_admin>', views.actualizar_about_images_admin, name='actualizar_about_images_admin'),
    path('eliminar_about_images_admin/<id_about_images_admin>', views.eliminar_about_images_admin, name='eliminar_about_images_admin'),
    path('footer_admin/', views.footer_admin, name='footer_admin'),
    path('donation_admin/', views.donation_admin, name='donation_admin'),
    path('post_admin/', views.post_admin, name='post_admin'),
    path('list_footer_admin_view/', views.list_footer_admin_view, name='list_footer_admin_view'),
    path('actualizar_footer_admin/<id_footer_admin>', views.actualizar_footer_admin, name='actualizar_footer_admin'),
    path('eliminar_footer_admin/<id_footer_admin>', views.eliminar_footer_admin, name='eliminar_footer_admin'),
    path('list_donation_admin_view/', views.list_donation_admin_view, name='list_donation_admin_view'),
    path('actualizar_donation_admin/<id_donation_admin>', views.actualizar_donation_admin, name='actualizar_donation_admin'),
    path('eliminar_donation_admin/<id_donation_admin>', views.eliminar_donation_admin, name='eliminar_donation_admin'),
    path('list_post_admin_view/', views.list_post_admin_view, name='list_post_admin_view'),
    path('actualizar_post_admin/<id_post_admin>', views.actualizar_post_admin, name='actualizar_post_admin'),
    path('eliminar_post_admin/<id_post_admin>', views.eliminar_post_admin, name='eliminar_post_admin'),
    path('page_admin/', views.page_admin, name='page_admin'),
    path('contact_info_admin/', views.contact_info_admin, name='contact_info_admin'),
    path('list_contact_info_admin_view/', views.list_contact_info_admin_view, name='list_contact_info_admin_view'),
    path('actualizar_contact_info_admin/<id_contact_info_admin>', views.actualizar_contact_info_admin, name='actualizar_contact_info_admin'),
    path('eliminar_contact_info_admin/<id_contact_info_admin>', views.eliminar_contact_info_admin, name='eliminar_contact_info_admin'),
    path('list_page_admin_view/', views.list_page_admin_view, name='list_page_admin_view'),
    path('actualizar_page_admin/<id_page_admin>', views.actualizar_page_admin, name='actualizar_page_admin'),
    path('eliminar_page_admin/<id_page_admin>', views.eliminar_page_admin, name='eliminar_page_admin'),
    path('best_videos_admin/', views.best_videos_admin, name='best_videos_admin'),
    path('list_best_videos_admin_view/', views.list_best_videos_admin_view, name='list_best_videos_admin_view'),
    path('actualizar_best_videos_admin/<id_best_videos_admin>', views.actualizar_best_videos_admin, name='actualizar_best_videos_admin'),
    path('eliminar_best_videos_admin/<id_best_videos_admin>', views.eliminar_best_videos_admin, name='eliminar_best_videos_admin'),
    path('best_videos/', views.best_videos, name='best_videos'),
    path('actualizar_nombre_tab/', views.actualizar_nombre_tab, name='actualizar_nombre_tab'),
    path('actualizar_nombre_tab_page/', views.actualizar_nombre_tab_page, name='actualizar_nombre_tab_page'),
    path('tab_admin/', views.tab_admin, name='tab_admin'),




]
