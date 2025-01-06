from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from datetime import datetime
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
import locale
from .forms import ContactMessageForm,AboutForm,ActivityForm, EventForm,Error404Form,SermonForm,BlogForm, TeamMemberForm, TestimonialForm, NewsletterForm
from django.core.exceptions import ValidationError
import json
from .models import ContactMessage, About, Activity, Event, Error404, Sermon, Blog, TeamMember, Testimonial

# Create your views here.

def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            # Guarda el email en la base de datos
            subscription = form.save(commit=False)
            email = subscription.email
            form.save()
            # Envía un correo de confirmación
            send_mail(
                'Subscription Confirmed',
                'Thank you for subscribing to our newsletter! with your email: ' + email,
                email,  # Email del remitente
                [email,'msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],
            )
            
            # Muestra un mensaje de éxito
            messages.success(request, 'Thank you for subscribing to our newsletter!')
            return redirect('home')  # Redirige para evitar el reenvío de formularios

        else:
            # Mensaje de error si el formulario no es válido
            messages.error(request, 'Please provide a valid email.')

    else:
        form = NewsletterForm()  # Cargar un formulario vacío en caso de GET

    return render(request, 'cars_reviews_app/home.html', {'form': form})

def privacy_policy(request):
    return render(request, 'mosque_web_app/privacy_policy.html')

def set_cookie_consent(request):
    response = JsonResponse({'status': 'ok'})
    response.set_cookie('cookie_consent', 'true', max_age=365*24*60*60)  # 1 año
    return response

def view_404(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/404.html',context )

def view_404_admin(request):
    if request.method == 'POST':
        form = Error404Form(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el registro en la base de datos
            form.save()
            
            # Obtener los datos del formulario
            events_404_error = form.cleaned_data['error']
            events_404_error_title = form.cleaned_data['error_title']
            events_404_error_description = form.cleaned_data['error_description']
            
            
            
            """
            # Enviar el correo electrónico
            send_mail(
                'Message from ' + message_name,  # Asunto
                message_message,  # Mensaje
                message_email,  # Correo electrónico del remitente
                ['msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com'],  # Correos de destino
            )
            """
            email_content = f"""
            You have received a new message  {events_404_error}:
            
            events_404_error_title: {events_404_error_title}
            events_404_error_description: {events_404_error_description}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {events_404_error}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            
            return render(request, 'mosque_web_app/404_admin.html', {'events_404_error_title': events_404_error_title})
    else:
        form = Error404Form()
    
    return render(request, 'mosque_web_app/404_admin.html', {'form': form})

def list_view_404_admin_view(request):
    la_lista_des_view_404_admin = Error404.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_view_404_admin_view.html', {'la_lista_des_view_404_admin': la_lista_des_view_404_admin})

def actualizar_view_404_admin(request, id_view_404_admin):
    view_404_admin = Error404.objects.get(pk=id_view_404_admin)
    form = Error404Form(request.POST or None, request.FILES or None,  instance=view_404_admin)
    if form.is_valid():
        form.save()
        return redirect('list_view_404_admin_view')
    context = {'view_404_admin': view_404_admin, 'form': form}
    return render(request, 'mosque_web_app/actualizar_view_404_admin.html', context)

def eliminar_view_404_admin(request, id_view_404_admin):
    view_404_admin = get_object_or_404(Error404, id=id_view_404_admin)
    view_404_admin.delete()
    messages.success(request, "El Error 404 ha sido eliminado con éxito.")
    return redirect('list_view_404_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def testimonial(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/testimonial.html',context )

def testimonial_admin(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial_social_links_data = form.cleaned_data.get('testimonial_social_links')
            try:
                # Convertir a JSON solo si es un string
                if isinstance(testimonial_social_links_data, str):
                    testimonial_social_links_data = json.loads(testimonial_social_links_data)
                    print(testimonial_social_links_data)
                elif isinstance(testimonial_social_links_data, dict):
                    # Si ya es un diccionario, lo dejamos tal cual
                    pass
                else:
                    raise ValidationError("Invalid format for social links.")
            except json.JSONDecodeError:
                return render(request, 'error_template.html', {
                    'error_message': "Invalid JSON format for social links."
                })
            # Guardar el registro en la base de datos
            testimonial  = form.save(commit=False)
            testimonial.user_creator_testimonial = request.user  # Asigna el usuario conectado
            testimonial.testimonial_social_links = testimonial_social_links_data
            testimonial.save()
            
            # Obtener los datos del formulario
            testimonial_full_name = form.cleaned_data['testimonial_full_name']
            testimonial_position = form.cleaned_data['testimonial_position']
            testimonial_status = form.cleaned_data['testimonial_status']
            testimonial_description = form.cleaned_data['testimonial_description']
            testimonial_date_of_birth = form.cleaned_data['testimonial_date_of_birth']
            testimonial_email = form.cleaned_data['testimonial_email']
            testimonial_phone_number = form.cleaned_data['testimonial_phone_number']
            testimonial_link = form.cleaned_data['testimonial_link']
            testimonial_img_url = form.cleaned_data['testimonial_img_url']
            testimonial_date = form.cleaned_data['testimonial_date']
            testimonial_time = form.cleaned_data['testimonial_time']
            testimonial_day = form.cleaned_data['testimonial_day']
            testimonial_social_links = form.cleaned_data['testimonial_social_links']
            
            """
            # Enviar el correo electrónico
            send_mail(
                'Message from ' + message_name,  # Asunto
                message_message,  # Mensaje
                message_email,  # Correo electrónico del remitente
                ['msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com'],  # Correos de destino
            )
            """
            email_content = f"""
            You have received a new message  {testimonial_full_name}:
            
            testimonial_position: {testimonial_position}
            testimonial_status: {testimonial_status}
            testimonial_description: {testimonial_description}
            testimonial_date_of_birth: {testimonial_date_of_birth}
            testimonial_email: {testimonial_email}
            testimonial_phone_number: {testimonial_phone_number}
            testimonial_link: {testimonial_link} 
            testimonial_img_url: {testimonial_img_url}
            testimonial_date: {testimonial_date}
            testimonial_time: {testimonial_time} comments
            testimonial_day: {testimonial_day}
            testimonial_social_links: {testimonial_social_links}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {testimonial_full_name}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            the_mosque_web_admin = f'{testimonial_full_name} - {testimonial_position} - {testimonial_status}'
            return render(request, 'mosque_web_app/mosque_web_admin.html', {'testimonial_full_name': testimonial_full_name, 'the_mosque_web_admin' : the_mosque_web_admin})
    else:
        form = TestimonialForm()
    
    return render(request, 'mosque_web_app/testimonial_admin.html', {'form': form})

def list_testimonial_admin_view(request):
    la_lista_testimonial_admin_view = Testimonial.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_testimonial_admin_view.html', {'la_lista_testimonial_admin_view': la_lista_testimonial_admin_view})

def actualizar_testimonial_admin(request, id_testimonial_admin):
    testimonial_admin = Testimonial.objects.get(pk=id_testimonial_admin)
    form = TestimonialForm(request.POST or None, request.FILES or None,  instance=testimonial_admin)
    if form.is_valid():
        form.save()
        return redirect('list_testimonial_admin_view')
    context = {'testimonial_admin': testimonial_admin, 'form': form}
    return render(request, 'mosque_web_app/actualizar_testimonial_admin.html', context)

def eliminar_testimonial_admin(request, id_testimonial_admin):
    testimonial_admin = get_object_or_404(Testimonial, id=id_testimonial_admin)
    testimonial_admin.delete()
    messages.success(request, "El Testimonial ha sido eliminado con éxito.")
    return redirect('list_testimonial_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal


def team(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/team.html',context )

def team_admin(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            social_links_data = form.cleaned_data.get('team_social_links')
            try:
                # Convertir a JSON solo si es un string
                if isinstance(social_links_data, str):
                    social_links_data = json.loads(social_links_data)
                    print(social_links_data)
                elif isinstance(social_links_data, dict):
                    # Si ya es un diccionario, lo dejamos tal cual
                    pass
                else:
                    raise ValidationError("Invalid format for social links.")
            except json.JSONDecodeError:
                return render(request, 'error_template.html', {
                    'error_message': "Invalid JSON format for social links."
                })
            # Guardar el registro en la base de datos
            team_member  = form.save(commit=False)
            team_member.user_creator_team_member = request.user  # Asigna el usuario conectado
            team_member.team_social_links = social_links_data
            team_member.save()
            
            # Obtener los datos del formulario
            team_full_name = form.cleaned_data['team_full_name']
            team_position = form.cleaned_data['team_position']
            team_status = form.cleaned_data['team_status']
            team_life_situation = form.cleaned_data['team_life_situation']
            team_description = form.cleaned_data['team_description']
            team_date_of_birth = form.cleaned_data['team_date_of_birth']
            team_email = form.cleaned_data['team_email']
            team_address = form.cleaned_data['team_address']
            team_phone_number = form.cleaned_data['team_phone_number']
            team_link = form.cleaned_data['team_link']
            team_img_url = form.cleaned_data['team_img_url']
            team_date_start = form.cleaned_data['team_date_start']
            team_time_start = form.cleaned_data['team_time_start']
            team_day_start = form.cleaned_data['team_day_start']
            team_social_links = form.cleaned_data['team_social_links']
            
            """
            # Enviar el correo electrónico
            send_mail(
                'Message from ' + message_name,  # Asunto
                message_message,  # Mensaje
                message_email,  # Correo electrónico del remitente
                ['msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com'],  # Correos de destino
            )
            """
            email_content = f"""
            You have received a new message  {team_full_name}:
            
            team_position: {team_position}
            team_status: {team_status}
            team_life_situation: {team_life_situation}
            team_description: {team_description}
            team_date_of_birth: {team_date_of_birth}
            team_email: {team_email}
            team_address: {team_address} 
            team_phone_number: {team_phone_number}
            team_link: {team_link}
            team_img_url: {team_img_url} 
            team_date_start: {team_date_start}
            team_time_start: {team_time_start}
            team_day_start: {team_day_start}
            team_social_links: {team_social_links}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {team_full_name}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            the_mosque_web_admin = f'{team_full_name} - {team_position} - {team_description}'
            return render(request, 'mosque_web_app/mosque_web_admin.html', {'team_full_name': team_full_name, 'the_mosque_web_admin' : the_mosque_web_admin})
    else:
        form = TeamMemberForm()
    
    return render(request, 'mosque_web_app/team_admin.html', {'form': form})

def list_team_admin_view(request):
    la_lista_team_admin_view = TeamMember.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_team_admin_view.html', {'la_lista_team_admin_view': la_lista_team_admin_view})

def actualizar_team_admin(request, id_team_admin):
    team_admin = TeamMember.objects.get(pk=id_team_admin)
    form = TeamMemberForm(request.POST or None, request.FILES or None,  instance=team_admin)
    if form.is_valid():
        form.save()
        return redirect('list_team_admin_view')
    context = {'team_admin': team_admin, 'form': form}
    return render(request, 'mosque_web_app/actualizar_team_admin.html', context)

def eliminar_team_admin(request, id_team_admin):
    team_admin = get_object_or_404(TeamMember, id=id_team_admin)
    team_admin.delete()
    messages.success(request, "El Team ha sido eliminado con éxito.")
    return redirect('list_team_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal



def blog(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/blog.html',context )

def blogs_admin(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el registro en la base de datos
            blog = form.save(commit=False)
            blog.user_blog = request.user  # Asigna el usuario conectado
            blog.save()
            
            # Obtener los datos del formulario
            blogs_blog_title = form.cleaned_data['blog_title']
            blogs_description_blog = form.cleaned_data['description_blog']
            blogs_link_blog = form.cleaned_data['link_blog']
            blogs_img_url_blog = form.cleaned_data['img_url_blog']
            blogs_date_blog = form.cleaned_data['date_blog']
            blogs_time_blog = form.cleaned_data['time_blog']
            blogs_day_blog = form.cleaned_data['day_blog']
            blogs_number_coments_blog = form.cleaned_data['number_coments_blog']
            
            
            """
            # Enviar el correo electrónico
            send_mail(
                'Message from ' + message_name,  # Asunto
                message_message,  # Mensaje
                message_email,  # Correo electrónico del remitente
                ['msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com'],  # Correos de destino
            )
            """
            email_content = f"""
            You have received a new message  {blogs_blog_title}:
            
            blogs_description_blog: {blogs_description_blog}
            blogs_link_blog: {blogs_link_blog}
            blogs_img_url_blog: {blogs_img_url_blog}
            blogs_date_blog: {blogs_date_blog}
            blogs_time_blog: {blogs_time_blog}
            blogs_day_blog: {blogs_day_blog}
            blogs_number_coments_blog: {blogs_number_coments_blog} comments
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {blogs_blog_title}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            the_mosque_web_admin = f'{blogs_blog_title} - {blogs_description_blog}'
            return render(request, 'mosque_web_app/mosque_web_admin.html', {'blogs_blog_title': blogs_blog_title, 'the_mosque_web_admin' : the_mosque_web_admin})
    else:
        form = BlogForm()
    
    return render(request, 'mosque_web_app/blogs_admin.html', {'form': form})

def list_blogs_admin_view(request):
    la_lista_blogs_admin_view = Blog.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_blogs_admin_view.html', {'la_lista_blogs_admin_view': la_lista_blogs_admin_view})

def actualizar_blogs_admin(request, id_blogs_admin):
    blogs_admin = Blog.objects.get(pk=id_blogs_admin)
    form = BlogForm(request.POST or None, request.FILES or None,  instance=blogs_admin)
    if form.is_valid():
        form.save()
        return redirect('list_blogs_admin_view')
    context = {'blogs_admin': blogs_admin, 'form': form}
    return render(request, 'mosque_web_app/actualizar_blogs_admin.html', context)

def eliminar_blogs_admin(request, id_blogs_admin):
    blogs_admin = get_object_or_404(Blog, id=id_blogs_admin)
    blogs_admin.delete()
    messages.success(request, "El Blog ha sido eliminado con éxito.")
    return redirect('list_blogs_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def sermon(request):
    sermons = Sermon.objects.all()  # Obtén todos los sermones
    context = {'sermons': sermons}
    #context = {'form': ''}
    return render(request, 'mosque_web_app/sermon.html',context )

def sermons_admin(request):
    if request.method == 'POST':
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el registro en la base de datos
            sermon = form.save(commit=False)
            sermon.user_sermon = request.user  # Asigna el usuario conectado
            sermon.save()
            
            # Obtener los datos del formulario
            sermons_sermon_title = form.cleaned_data['sermon_title']
            sermons_description_sermon = form.cleaned_data['description_sermon']
            sermons_link_sermon = form.cleaned_data['link_sermon']
            sermons_img_url_sermon = form.cleaned_data['img_url_sermon']
            sermons_date_sermon = form.cleaned_data['date_sermon']
            sermons_time_sermon = form.cleaned_data['time_sermon']
            sermons_day_sermon = form.cleaned_data['day_sermon']
            sermons_file_sermon = form.cleaned_data['file_sermon']
            
            
            """
            # Enviar el correo electrónico
            send_mail(
                'Message from ' + message_name,  # Asunto
                message_message,  # Mensaje
                message_email,  # Correo electrónico del remitente
                ['msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com'],  # Correos de destino
            )
            """
            email_content = f"""
            You have received a new message  {sermons_sermon_title}:
            
            sermons_description_sermon: {sermons_description_sermon}
            sermons_link_sermon: {sermons_link_sermon}
            sermons_img_url_sermon: {sermons_img_url_sermon}
            sermons_date_sermon: {sermons_date_sermon}
            sermons_time_sermon: {sermons_time_sermon}
            sermons_day_sermon: {sermons_day_sermon}
            sermons_file_sermon: {sermons_file_sermon}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {sermons_sermon_title}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            the_mosque_web_admin = f'{sermons_sermon_title} - {sermons_description_sermon}'
            return render(request, 'mosque_web_app/mosque_web_admin.html', {'sermons_sermon_title': sermons_sermon_title, 'the_mosque_web_admin' : the_mosque_web_admin})
    else:
        form = SermonForm()
    
    return render(request, 'mosque_web_app/sermons_admin.html', {'form': form})

def list_sermons_admin_view(request):
    la_lista_sermons_admin_view = Sermon.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_sermons_admin_view.html', {'la_lista_sermons_admin_view': la_lista_sermons_admin_view})

def actualizar_sermons_admin(request, id_sermons_admin):
    sermons_admin = Sermon.objects.get(pk=id_sermons_admin)
    form = SermonForm(request.POST or None, request.FILES or None,  instance=sermons_admin)
    if form.is_valid():
        form.save()
        return redirect('list_sermons_admin_view')
    context = {'sermons_admin': sermons_admin, 'form': form}
    return render(request, 'mosque_web_app/actualizar_sermons_admin.html', context)

def eliminar_sermons_admin(request, id_sermons_admin):
    sermons_admin = get_object_or_404(Sermon, id=id_sermons_admin)
    sermons_admin.delete()
    messages.success(request, "El Sermon ha sido eliminado con éxito.")
    return redirect('list_sermons_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def event(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/event.html',context )

def events_admin(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el registro en la base de datos
            form.save()
            
            # Obtener los datos del formulario
            events_title_event = form.cleaned_data['title_event']
            events_description_title_event = form.cleaned_data['description_title_event']
            events_link_event = form.cleaned_data['link_event']
            events_img_url_event = form.cleaned_data['img_url_event']
            events_date_event = form.cleaned_data['date_event']
            events_time_event = form.cleaned_data['time_event']
            events_day_event = form.cleaned_data['day_event']
            events_file_event = form.cleaned_data['file_event']
            
            
            """
            # Enviar el correo electrónico
            send_mail(
                'Message from ' + message_name,  # Asunto
                message_message,  # Mensaje
                message_email,  # Correo electrónico del remitente
                ['msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com'],  # Correos de destino
            )
            """
            email_content = f"""
            You have received a new message  {events_title_event}:
            
            events_description_title_event: {events_description_title_event}
            events_link_event: {events_link_event}
            events_img_url_event: {events_img_url_event}
            events_date_event: {events_date_event}
            events_time_event: {events_time_event}
            events_day_event: {events_day_event}
            events_file_event: {events_file_event}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {events_title_event}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            
            return render(request, 'mosque_web_app/events_admin.html', {'events_title_event': events_title_event})
    else:
        form = EventForm()
    
    return render(request, 'mosque_web_app/events_admin.html', {'form': form})

def list_events_admin_view(request):
    la_lista_events_admin_view = Event.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_events_admin_view.html', {'la_lista_events_admin_view': la_lista_events_admin_view})

def actualizar_events_admin(request, id_events_admin):
    events_admin = Event.objects.get(pk=id_events_admin)
    form = EventForm(request.POST or None, request.FILES or None,  instance=events_admin)
    if form.is_valid():
        form.save()
        return redirect('list_events_admin_view')
    context = {'events_admin': events_admin, 'form': form}
    return render(request, 'mosque_web_app/actualizar_events_admin.html', context)

def eliminar_events_admin(request, id_events_admin):
    events_admin = get_object_or_404(Event, id=id_events_admin)
    events_admin.delete()
    messages.success(request, "El Event ha sido eliminado con éxito.")
    return redirect('list_events_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def activity(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/activity.html',context )

def activities_admin(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            # Guardar el registro en la base de datos
            form.save()
            
            # Obtener los datos del formulario
            activities_activity_title = form.cleaned_data['activity_title']
            activities_activity_mosque_development = form.cleaned_data['activity_mosque_development']
            activities_description_activity_mosque_development = form.cleaned_data['description_activity_mosque_development']
            activities_activity_charity_donation = form.cleaned_data['activity_charity_donation']
            activities_description_activity_charity_donation = form.cleaned_data['description_activity_charity_donation']
            activities_activity_quran_learning = form.cleaned_data['activity_quran_learning']
            activities_description_activity_quran_learning = form.cleaned_data['description_activity_quran_learning']
            activities_activity_hadith_sunnah = form.cleaned_data['activity_hadith_sunnah']
            activities_description_activity_hadith_sunnah = form.cleaned_data['description_activity_hadith_sunnah']
            activities_activity_parent_education = form.cleaned_data['activity_parent_education']
            activities_description_activity_parent_education = form.cleaned_data['description_activity_parent_education']
            activities_activity_help_orphans = form.cleaned_data['activity_help_orphans']
            activities_description_activity_help_orphans = form.cleaned_data['description_activity_help_orphans']
            activities_activity_testimonial = form.cleaned_data['activity_testimonial']
            activities_activity_title_testimonial = form.cleaned_data['activity_title_testimonial']
            
            
            """
            # Enviar el correo electrónico
            send_mail(
                'Message from ' + message_name,  # Asunto
                message_message,  # Mensaje
                message_email,  # Correo electrónico del remitente
                ['msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com'],  # Correos de destino
            )
            """
            email_content = f"""
            You have received a new message  {activities_activity_title}:
            
            activities_activity_mosque_development: {activities_activity_mosque_development}
            activities_description_activity_mosque_development: {activities_description_activity_mosque_development}
            activities_activity_charity_donation: {activities_activity_charity_donation}
            activities_description_activity_charity_donation: {activities_description_activity_charity_donation}
            activities_activity_quran_learning: {activities_activity_quran_learning}
            activities_description_activity_quran_learning: {activities_description_activity_quran_learning}
            activities_activity_hadith_sunnah: {activities_activity_hadith_sunnah}
            activities_description_activity_hadith_sunnah: {activities_description_activity_hadith_sunnah}
            activities_activity_parent_education: {activities_activity_parent_education}
            activities_description_activity_parent_education: {activities_description_activity_parent_education}
            activities_activity_help_orphans: {activities_activity_help_orphans}
            activities_description_activity_help_orphans: {activities_description_activity_help_orphans}
            activities_activity_testimonial: {activities_activity_testimonial}
            activities_activity_title_testimonial: {activities_activity_title_testimonial}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {activities_activity_title}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            
            return render(request, 'mosque_web_app/activities_admin.html', {'activities_activity_title': activities_activity_title})
    else:
        form = ActivityForm()
    
    return render(request, 'mosque_web_app/activities_admin.html', {'form': form})

def list_activities_admin_view(request):
    la_lista_activities_admin_view = Activity.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_activities_admin_view.html', {'la_lista_activities_admin_view': la_lista_activities_admin_view})

def actualizar_activities_admin(request, id_activities_admin):
    activities_admin = Activity.objects.get(pk=id_activities_admin)
    form = ActivityForm(request.POST or None, request.FILES or None,  instance=activities_admin)
    if form.is_valid():
        form.save()
        return redirect('list_activities_admin_view')
    context = {'activities_admin': activities_admin, 'form': form}
    return render(request, 'mosque_web_app/actualizar_activities_admin.html', context)

def eliminar_activities_admin(request, id_activities_admin):
    activities_admin = get_object_or_404(Activity, id=id_activities_admin)
    activities_admin.delete()
    messages.success(request, "El Activities ha sido eliminado con éxito.")
    return redirect('list_activities_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def about(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/about.html',context )

def about_admin(request):
    if request.method == 'POST':
        form = AboutForm(request.POST)
        if form.is_valid():
            # Guardar el registro en la base de datos
            form.save()
            
            # Obtener los datos del formulario
            about_about_the_mosque = form.cleaned_data['about_the_mosque']
            about_allah_helps_those = form.cleaned_data['allah_helps_those']
            about_description_about = form.cleaned_data['description_about']
            about_our_vision = form.cleaned_data['our_vision']
            about_description_our_vision = form.cleaned_data['description_our_vision']
            about_our_mission = form.cleaned_data['our_mission']
            about_description_our_mission = form.cleaned_data['description_our_mission']
            about_raised = form.cleaned_data['raised']
            about_raised_value = form.cleaned_data['raised_value']
            about_description_raised = form.cleaned_data['description_raised']
            about_charity_and_donation = form.cleaned_data['charity_and_donation']
            about_parent_education = form.cleaned_data['parent_education']
            about_hadith_and_sunnah = form.cleaned_data['hadith_and_sunnah']
            about_mosque_development = form.cleaned_data['mosque_development']
            
            """
            # Enviar el correo electrónico
            send_mail(
                'Message from ' + message_name,  # Asunto
                message_message,  # Mensaje
                message_email,  # Correo electrónico del remitente
                ['msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com'],  # Correos de destino
            )
            """
            email_content = f"""
            You have received a new message  {about_about_the_mosque}:
            
            about_allah_helps_those: {about_allah_helps_those}
            about_description_about: {about_description_about}
            about_our_vision: {about_our_vision}
            about_description_our_vision: {about_description_our_vision}
            about_our_mission: {about_our_mission}
            about_description_our_mission: {about_description_our_mission}
            about_raised: {about_raised}
            about_raised_value: {about_raised_value}
            about_description_raised: {about_description_raised}
            about_charity_and_donation: {about_charity_and_donation}
            about_parent_education: {about_parent_education}
            about_hadith_and_sunnah: {about_hadith_and_sunnah}
            about_mosque_development: {about_mosque_development}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {about_about_the_mosque}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            
            return render(request, 'mosque_web_app/about_admin.html', {'about_about_the_mosque': about_about_the_mosque})
    else:
        form = AboutForm()
    
    return render(request, 'mosque_web_app/about_admin.html', {'form': form})

def list_about_admin_view(request):
    la_lista_about_admin_view = About.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_about_admin_view.html', {'la_lista_about_admin_view': la_lista_about_admin_view})

def actualizar_about_admin(request, id_about_admin):
    about_admin = About.objects.get(pk=id_about_admin)
    form = AboutForm(request.POST or None, request.FILES or None,  instance=about_admin)
    if form.is_valid():
        form.save()
        return redirect('list_about_admin_view')
    context = {'about_admin': about_admin, 'form': form}
    return render(request, 'mosque_web_app/actualizar_about_admin.html', context)

def eliminar_about_admin(request, id_about_admin):
    about_admin = get_object_or_404(About, id=id_about_admin)
    about_admin.delete()
    messages.success(request, "El About ha sido eliminado con éxito.")
    return redirect('list_about_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def contact1(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/contact.html',context )

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # Guardar el registro en la base de datos
            form.save()
            
            # Obtener los datos del formulario
            message_name = form.cleaned_data['name']
            message_email = form.cleaned_data['email']
            message_subject = form.cleaned_data['subject']
            message_message = form.cleaned_data['message']
            
            """
            # Enviar el correo electrónico
            send_mail(
                'Message from ' + message_name,  # Asunto
                message_message,  # Mensaje
                message_email,  # Correo electrónico del remitente
                ['msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com'],  # Correos de destino
            )
            """
            email_content = f"""
            You have received a new contact message from {message_name}:

            Name: {message_name}
            Email: {message_email}
            Subject: {message_subject}
            Message: {message_message}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {message_name}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                message_email,  # Correo electrónico del remitente
                [message_email,'msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            
            return render(request, 'mosque_web_app/contact.html', {'message_name': message_name})
    else:
        form = ContactMessageForm()
    
    return render(request, 'mosque_web_app/contact.html', {'form': form})

def list_contact_view(request):
    la_lista_contact_view = ContactMessage.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_contact_view.html', {'la_lista_contact_view': la_lista_contact_view})

def actualizar_contact(request, id_contact):
    contact = ContactMessage.objects.get(pk=id_contact)
    form = ContactMessageForm(request.POST or None, request.FILES or None,  instance=contact)
    if form.is_valid():
        form.save()
        return redirect('list_contact_view')
    context = {'contact': contact, 'form': form}
    return render(request, 'mosque_web_app/actualizar_contact.html', context)

def eliminar_contact(request, id_contact):
    contact = get_object_or_404(ContactMessage, id=id_contact)
    contact.delete()
    messages.success(request, "El Contact ha sido eliminado con éxito.")
    return redirect('list_contact_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def mosque_web_admin_view(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/mosque_web_admin.html',context )

def custom_logout_view(request):
    logout(request)
    return redirect('home') 

def home(request):
    fecha_actual = datetime.now().strftime('%A, %B %d, %Y')  # Ejemplo: Monday, January 01, 2045
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Configura a español
        fecha_actual_es = datetime.now().strftime('%A, %d de %B de %Y') 
    except locale.Error:
        # Si no se puede establecer el locale, usa un formato alternativo
        fecha_actual_es = datetime.now().strftime('%A, %d of %B of %Y')
    
    fecha_hora_actual = datetime.now().strftime('%A, %B %d, %Y %I:%M:%S %p') 
    context = {
        'fecha_actual': fecha_actual,
        'fecha_actual_es': fecha_actual_es,
        'fecha_hora_actual': fecha_hora_actual
    }
    return render(request, 'mosque_web_app/home.html', context)