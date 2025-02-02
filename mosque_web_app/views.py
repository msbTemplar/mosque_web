from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from datetime import datetime
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
import locale
from .forms import ContactMessageForm,AboutForm,ActivityForm, EventForm,Error404Form,SermonForm,BlogForm, TeamMemberForm, TestimonialForm, NewsletterForm, AboutImagesForm, FooterForm, DonationForm, PostForm, ContactInfoForm, PageForm,CustomUserCreationForm, BestVideosForm, TabForm
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json
from .models import ContactMessage, About, Activity, Event, Error404, Sermon, Blog, TeamMember, Testimonial, AboutImages, Footer, Donation, Post, ContactInfo, Page, BestVideos, Tab, TabPage
from django.contrib.auth.views import LoginView
from django.views.decorators.cache import cache_page
# Create your views here.

@csrf_exempt
def actualizar_nombre_tab(request):
    if request.method == "POST":
        tab_id = request.POST.get("tab_id")
        nuevo_nombre = request.POST.get("nuevo_nombre", "").strip()

        if not nuevo_nombre:
            return JsonResponse({"status": "error", "message": "El nombre no puede estar vacío."})

        try:
            tab = Tab.objects.get(id=tab_id)
            tab.tab_nombre = nuevo_nombre
            tab.save()
            return JsonResponse({"status": "success", "nuevo_nombre": nuevo_nombre})
        except Tab.DoesNotExist:
            return JsonResponse({"status": "error", "message": "No se encontró la pestaña."}, status=404)

    return JsonResponse({"status": "error", "message": "Método no permitido."}, status=400)


@csrf_exempt
def actualizar_nombre_tab_page(request):
    if request.method == "POST":
        page_id = request.POST.get("page_id")
        nuevo_nombre = request.POST.get("nuevo_nombre", "").strip()

        if not nuevo_nombre:
            return JsonResponse({"status": "error", "message": "El nombre no puede estar vacío."})

        try:
            tab_page = TabPage.objects.get(id=page_id)
            tab_page.tab_page_name = nuevo_nombre
            tab_page.save()
            return JsonResponse({"status": "success", "nuevo_nombre": nuevo_nombre})
        except TabPage.DoesNotExist:
            return JsonResponse({"status": "error", "message": "No se encontró la pestaña."}, status=404)

    return JsonResponse({"status": "error", "message": "Método no permitido."}, status=400)


def register1(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu cuenta ha sido creada con éxito!")
            return redirect('login')  # Redirige a la página de login después de registrarse
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'cars_reviews_app/register.html', {'form': form})


def register(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )

    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()

    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None

    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "¡Tu cuenta ha sido creada con éxito!")

            # Enviar correo electrónico de bienvenida
            email_content = f"""
            ¡Bienvenido {user.username}!

            Tu cuenta ha sido creada con éxito en nuestro sitio web.

            Gracias por unirte a nuestra comunidad.
            """

            send_mail(
                'Bienvenido a nuestro sitio web',  # Asunto
                email_content,  # Cuerpo del correo
                'noreply@tusitio.com',  # Correo electrónico del remitente
                [user.email,'msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correo electrónico del usuario registrado
            )

            return redirect('login')  # Redirige a la página de login después de registrarse
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {
        'form': form,
        'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,
    })



class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la última página activa
        page = (
            Page.objects.filter(is_active=True)
            .order_by('-updated_at', '-created_at')
            .first()
        )

        # Obtener la última información de contacto activa
        contact_info = (
            ContactInfo.objects.filter(is_active=True)
            .order_by('-updated_at', '-created_at')
            .first()
        )
        tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
        
        tab_pages = TabPage.objects.all()

        # Obtener el último footer (si existe)
        footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

        # Obtener todos los posts
        posts = Post.objects.all() if Post.objects.exists() else None

        # Obtener todas las donaciones
        donations = Donation.objects.all() if Donation.objects.exists() else None

        # Variables relacionadas con el footer
        footer_subscribe_footer = getattr(footer, 'subscribe_footer', 'No footer available')
        footer_description_subscribe_footer = getattr(footer, 'description_subscribe_footer', 'No description available.')
        footer_subscibe_boton_footer = getattr(footer, 'subscibe_boton_footer', 'Subscribe')
        footer_themosque_footer = getattr(footer, 'themosque_footer', 'No footer description.')
        footer_link_footer = getattr(footer, 'link_footer', '#')
        footer_our_mosque_footer = getattr(footer, 'our_mosque_footer', 'No mosque info.')
        footer_our_address_footer = getattr(footer, 'our_address_footer', 'No address.')
        footer_our_mobile_footer = getattr(footer, 'our_mobile_footer', 'No mobile info.')
        footer_our_mobile_mobile_footer = getattr(footer, 'our_mobile_mobile_footer', 'No phone info.')
        footer_site_name_footer = getattr(footer, 'site_name_footer', 'Website')

        # Actualizar el contexto
        context.update({
            'donations': donations,
            'posts': posts,
            'footer': footer,
            'footer_subscribe_footer': footer_subscribe_footer,
            'footer_description_subscribe_footer': footer_description_subscribe_footer,
            'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
            'footer_themosque_footer': footer_themosque_footer,
            'footer_link_footer': footer_link_footer,
            'footer_our_mosque_footer': footer_our_mosque_footer,
            'footer_our_address_footer': footer_our_address_footer,
            'footer_our_mobile_footer': footer_our_mobile_footer,
            'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
            'footer_site_name_footer': footer_site_name_footer,
            'contact_info': contact_info,
            'page': page,
            'tabs': tabs,
            'tab_pages': tab_pages,
        })

        return context



def newsletter(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
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

    return render(request, 'cars_reviews_app/home.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def privacy_policy(request):
    return render(request, 'mosque_web_app/privacy_policy.html')

def set_cookie_consent(request):
    response = JsonResponse({'status': 'ok'})
    response.set_cookie('cookie_consent', 'true', max_age=365*24*60*60)  # 1 año
    return response

def view_404(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    error_data = Error404.objects.last() if Error404.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    context = {'form': '','donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'error_data': error_data,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/404.html',context )

def view_404_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None
    
    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
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
            
            return render(request, 'mosque_web_app/404_admin.html', {'events_404_error_title': events_404_error_title,'donations': donations,
            'posts': posts,
            'footer': footer,
            'footer_subscribe_footer': footer_subscribe_footer,
            'footer_description_subscribe_footer': footer_description_subscribe_footer,
            'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
            'footer_themosque_footer': footer_themosque_footer,
            'footer_link_footer': footer_link_footer,
            'footer_our_mosque_footer': footer_our_mosque_footer,
            'footer_our_address_footer': footer_our_address_footer,
            'footer_our_mobile_footer': footer_our_mobile_footer,
            'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
            'footer_site_name_footer': footer_site_name_footer,
            'contact_info': contact_info,
            'page': page,
            'tabs': tabs,
            'tab_pages': tab_pages,})
    else:
        form = Error404Form()
    
    return render(request, 'mosque_web_app/404_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_view_404_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_des_view_404_admin = Error404.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_view_404_admin_view.html', {'la_lista_des_view_404_admin': la_lista_des_view_404_admin,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_view_404_admin(request, id_view_404_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    view_404_admin = Error404.objects.get(pk=id_view_404_admin)
    form = Error404Form(request.POST or None, request.FILES or None,  instance=view_404_admin)
    if form.is_valid():
        form.save()
        return redirect('list_view_404_admin_view')
    context = {'view_404_admin': view_404_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_view_404_admin.html', context)

def eliminar_view_404_admin(request, id_view_404_admin):
    view_404_admin = get_object_or_404(Error404, id=id_view_404_admin)
    view_404_admin.delete()
    messages.success(request, "El Error 404 ha sido eliminado con éxito.")
    return redirect('list_view_404_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def testimonial(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    testimonials  = Testimonial.objects.all().order_by('-testimonial_date', '-testimonial_time') if Testimonial.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    context = {'form': '','donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'testimonials': testimonials,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/testimonial.html',context )

def testimonial_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
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
            return render(request, 'mosque_web_app/mosque_web_admin.html', {'testimonial_full_name': testimonial_full_name, 'the_mosque_web_admin' : the_mosque_web_admin,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})
    else:
        form = TestimonialForm()
    
    return render(request, 'mosque_web_app/testimonial_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_testimonial_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_testimonial_admin_view = Testimonial.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_testimonial_admin_view.html', {'la_lista_testimonial_admin_view': la_lista_testimonial_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_testimonial_admin(request, id_testimonial_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    testimonial_admin = Testimonial.objects.get(pk=id_testimonial_admin)
    form = TestimonialForm(request.POST or None, request.FILES or None,  instance=testimonial_admin)
    if form.is_valid():
        form.save()
        return redirect('list_testimonial_admin_view')
    context = {'testimonial_admin': testimonial_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_testimonial_admin.html', context)

def eliminar_testimonial_admin(request, id_testimonial_admin):
    testimonial_admin = get_object_or_404(Testimonial, id=id_testimonial_admin)
    testimonial_admin.delete()
    messages.success(request, "El Testimonial ha sido eliminado con éxito.")
    return redirect('list_testimonial_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal


def team(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    context = {'form': '','donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/team.html',context )

def team_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
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
            return render(request, 'mosque_web_app/mosque_web_admin.html', {'team_full_name': team_full_name, 'the_mosque_web_admin' : the_mosque_web_admin,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})
    else:
        form = TeamMemberForm()
    
    return render(request, 'mosque_web_app/team_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_team_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_team_admin_view = TeamMember.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_team_admin_view.html', {'la_lista_team_admin_view': la_lista_team_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_team_admin(request, id_team_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    team_admin = TeamMember.objects.get(pk=id_team_admin)
    form = TeamMemberForm(request.POST or None, request.FILES or None,  instance=team_admin)
    if form.is_valid():
        form.save()
        return redirect('list_team_admin_view')
    context = {'team_admin': team_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_team_admin.html', context)

def eliminar_team_admin(request, id_team_admin):
    team_admin = get_object_or_404(TeamMember, id=id_team_admin)
    team_admin.delete()
    messages.success(request, "El Team ha sido eliminado con éxito.")
    return redirect('list_team_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal



def blog(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    blogs = Blog.objects.all().order_by('-date_blog', '-time_blog') if Blog.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    context = {'form': '','donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page, 'blogs': blogs,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/blog.html',context )

def blogs_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
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
            return render(request, 'mosque_web_app/mosque_web_admin.html', {'blogs_blog_title': blogs_blog_title, 'the_mosque_web_admin' : the_mosque_web_admin,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})
    else:
        form = BlogForm()
    
    return render(request, 'mosque_web_app/blogs_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_blogs_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_blogs_admin_view = Blog.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_blogs_admin_view.html', {'la_lista_blogs_admin_view': la_lista_blogs_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,
        })

def actualizar_blogs_admin(request, id_blogs_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    blogs_admin = Blog.objects.get(pk=id_blogs_admin)
    form = BlogForm(request.POST or None, request.FILES or None,  instance=blogs_admin)
    if form.is_valid():
        form.save()
        return redirect('list_blogs_admin_view')
    context = {'blogs_admin': blogs_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_blogs_admin.html', context)

def eliminar_blogs_admin(request, id_blogs_admin):
    blogs_admin = get_object_or_404(Blog, id=id_blogs_admin)
    blogs_admin.delete()
    messages.success(request, "El Blog ha sido eliminado con éxito.")
    return redirect('list_blogs_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def sermon(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    sermons = Sermon.objects.all()  # Obtén todos los sermones
    context = {'sermons': sermons,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    #context = {'form': ''}
    return render(request, 'mosque_web_app/sermon.html',context )

def sermons_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
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
            return render(request, 'mosque_web_app/mosque_web_admin.html', {'sermons_sermon_title': sermons_sermon_title, 'the_mosque_web_admin' : the_mosque_web_admin,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})
    else:
        form = SermonForm()
    
    return render(request, 'mosque_web_app/sermons_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_sermons_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_sermons_admin_view = Sermon.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_sermons_admin_view.html', {'la_lista_sermons_admin_view': la_lista_sermons_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_sermons_admin(request, id_sermons_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    sermons_admin = Sermon.objects.get(pk=id_sermons_admin)
    form = SermonForm(request.POST or None, request.FILES or None,  instance=sermons_admin)
    if form.is_valid():
        form.save()
        return redirect('list_sermons_admin_view')
    context = {'sermons_admin': sermons_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_sermons_admin.html', context)

def eliminar_sermons_admin(request, id_sermons_admin):
    sermons_admin = get_object_or_404(Sermon, id=id_sermons_admin)
    sermons_admin.delete()
    messages.success(request, "El Sermon ha sido eliminado con éxito.")
    return redirect('list_sermons_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def event(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    events = Event.objects.all() if Event.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    
    context = {'form': '','donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page, 'events': events,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/event.html',context )

def events_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
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
            
            return render(request, 'mosque_web_app/events_admin.html', {'events_title_event': events_title_event,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})
    else:
        form = EventForm()
    
    return render(request, 'mosque_web_app/events_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_events_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_events_admin_view = Event.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_events_admin_view.html', {'la_lista_events_admin_view': la_lista_events_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_events_admin(request, id_events_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    events_admin = Event.objects.get(pk=id_events_admin)
    form = EventForm(request.POST or None, request.FILES or None,  instance=events_admin)
    if form.is_valid():
        form.save()
        return redirect('list_events_admin_view')
    context = {'events_admin': events_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_events_admin.html', context)

def eliminar_events_admin(request, id_events_admin):
    events_admin = get_object_or_404(Event, id=id_events_admin)
    events_admin.delete()
    messages.success(request, "El Event ha sido eliminado con éxito.")
    return redirect('list_events_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def activity(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    testimonials = Testimonial.objects.all() if Testimonial.objects.exists() else None
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    last_activity = Activity.objects.order_by('-id').first() if Activity.objects.exists() else None
    
    
    context = {'form': '','donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,'last_activity': last_activity, 'testimonials': testimonials,'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/activity.html',context )

def activities_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
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
            
            return render(request, 'mosque_web_app/activities_admin.html', {'activities_activity_title': activities_activity_title,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})
    else:
        form = ActivityForm()
    
    return render(request, 'mosque_web_app/activities_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_activities_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_activities_admin_view = Activity.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_activities_admin_view.html', {'la_lista_activities_admin_view': la_lista_activities_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_activities_admin(request, id_activities_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    activities_admin = Activity.objects.get(pk=id_activities_admin)
    form = ActivityForm(request.POST or None, request.FILES or None,  instance=activities_admin)
    if form.is_valid():
        form.save()
        return redirect('list_activities_admin_view')
    context = {'activities_admin': activities_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_activities_admin.html', context)

def eliminar_activities_admin(request, id_activities_admin):
    activities_admin = get_object_or_404(Activity, id=id_activities_admin)
    activities_admin.delete()
    messages.success(request, "El Activities ha sido eliminado con éxito.")
    return redirect('list_activities_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

""" def about(request):
    abouts = About.objects.all()  # Obtén todos los sermones
    context = {'abouts': abouts}
    #context = {'form': ''}
    return render(request, 'mosque_web_app/about.html',context ) """

def about(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    abouts_images = AboutImages.objects.all()
    team_members = TeamMember.objects.all()
    for member in team_members:
        if member.team_social_links:
            # Asegúrate de que sea un diccionario válido
            if isinstance(member.team_social_links, str):
                try:
                    member.team_social_links = json.loads(member.team_social_links)
                except json.JSONDecodeError:
                    member.team_social_links = {}
            elif not isinstance(member.team_social_links, dict):
                member.team_social_links = {}
        else:
            member.team_social_links = {}
    president = TeamMember.objects.filter(team_position="President").first()  # Obtén el presidente (si existe)
    other_members = TeamMember.objects.exclude(team_position="President")  # Excluye al presidente
 
    try:
        about = About.objects.latest('id')  # Obtiene el último registro basado en el campo 'id'
    except About.DoesNotExist:
        about = None  # Maneja el caso donde no hay registros en la base de datos
    context = {'about': about, 'abouts_images': abouts_images, 'team_members': team_members, 'president': president,
        'other_members': other_members,
        'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,
        }
    return render(request, 'mosque_web_app/about.html', context)


def about_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES)
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
            about_img_url_raised_about = form.cleaned_data['img_url_raised_about']
            about_charity_and_donation = form.cleaned_data['charity_and_donation']
            about_parent_education = form.cleaned_data['parent_education']
            about_hadith_and_sunnah = form.cleaned_data['hadith_and_sunnah']
            about_mosque_development = form.cleaned_data['mosque_development']
            about_file_about = form.cleaned_data['file_about']
            
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
            about_img_url_raised_about: {about_img_url_raised_about}
            about_charity_and_donation: {about_charity_and_donation}
            about_parent_education: {about_parent_education}
            about_hadith_and_sunnah: {about_hadith_and_sunnah}
            about_mosque_development: {about_mosque_development}
            about_file_about: {about_file_about}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {about_about_the_mosque}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            
            return render(request, 'mosque_web_app/about_admin.html', {'about_about_the_mosque': about_about_the_mosque,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})
    else:
        form = AboutForm()
    
    return render(request, 'mosque_web_app/about_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_about_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_about_admin_view = About.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_about_admin_view.html', {'la_lista_about_admin_view': la_lista_about_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_about_admin(request, id_about_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    about_admin = About.objects.get(pk=id_about_admin)
    form = AboutForm(request.POST or None, request.FILES or None,  instance=about_admin)
    if form.is_valid():
        form.save()
        return redirect('list_about_admin_view')
    context = {'about_admin': about_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_about_admin.html', context)

def eliminar_about_admin(request, id_about_admin):
    about_admin = get_object_or_404(About, id=id_about_admin)
    about_admin.delete()
    messages.success(request, "El About ha sido eliminado con éxito.")
    return redirect('list_about_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def about_images_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    if request.method == 'POST':
        form = AboutImagesForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el registro en la base de datos
            form.save()
            
            # Obtener los datos del formulario
            about_images_the_about_image = form.cleaned_data['about_images_the_about_image']
            img_url_about_images = form.cleaned_data['img_url_about_images']
            
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
            You have received a new message  {about_images_the_about_image}:
            
            about_images_the_about_image: {about_images_the_about_image}
            img_url_about_images: {img_url_about_images}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'Message from {about_images_the_about_image}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            
            return render(request, 'mosque_web_app/about_images_admin.html', {'about_images_the_about_image': about_images_the_about_image,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})
    else:
        form = AboutImagesForm()
    
    return render(request, 'mosque_web_app/about_images_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_about_images_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_about_images_admin_view = AboutImages.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_about_images_admin_view.html', {'la_lista_about_images_admin_view': la_lista_about_images_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_about_images_admin(request, id_about_images_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    about_images_admin = AboutImages.objects.get(pk=id_about_images_admin)
    form = AboutImagesForm(request.POST or None, request.FILES or None,  instance=about_images_admin)
    if form.is_valid():
        form.save()
        return redirect('list_about_images_admin_view')
    context = {'about_images_admin': about_images_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_about_images_admin.html', context)

def eliminar_about_images_admin(request, id_about_images_admin):
    about_images_admin = get_object_or_404(AboutImages, id=id_about_images_admin)
    about_images_admin.delete()
    messages.success(request, "El About images ha sido eliminado con éxito.")
    return redirect('list_about_images_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

def contact1(request):
    context = {'form': ''}
    return render(request, 'mosque_web_app/contact.html',context )

def contact(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
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
            
            return render(request, 'mosque_web_app/contact.html', {'message_name': message_name,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})
    else:
        form = ContactMessageForm()
    
    return render(request, 'mosque_web_app/contact.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_contact_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_contact_view = ContactMessage.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_contact_view.html', {'la_lista_contact_view': la_lista_contact_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_contact(request, id_contact):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    contact = ContactMessage.objects.get(pk=id_contact)
    form = ContactMessageForm(request.POST or None, request.FILES or None,  instance=contact)
    if form.is_valid():
        form.save()
        return redirect('list_contact_view')
    context = {'contact': contact, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_contact.html', context)

def eliminar_contact(request, id_contact):
    contact = get_object_or_404(ContactMessage, id=id_contact)
    contact.delete()
    messages.success(request, "El Contact ha sido eliminado con éxito.")
    return redirect('list_contact_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal


def footer_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    if request.method == 'POST':
        form = FooterForm(request.POST, request.FILES)  # Aseguramos que los archivos también se manejen
        if form.is_valid():
            # Guardar el objeto Footer en la base de datos
            footer1 = form.save()

            # Obtener los datos del formulario
            title_footer = form.cleaned_data['title_footer']
            description_footer = form.cleaned_data['description_footer']
            link_footer = form.cleaned_data['link_footer']
            subscribe_footer = form.cleaned_data['subscribe_footer']
            description_subscribe_footer = form.cleaned_data['description_subscribe_footer']
            subscibe_boton_footer = form.cleaned_data['subscibe_boton_footer']
            themosque_footer = form.cleaned_data['themosque_footer']
            themosque_description_footer = form.cleaned_data['themosque_description_footer']
            our_mosque_footer = form.cleaned_data['our_mosque_footer']
            our_address_footer = form.cleaned_data['our_address_footer']
            our_address_address_footer = form.cleaned_data['our_address_address_footer']
            our_mobile_footer = form.cleaned_data['our_mobile_footer']
            our_mobile_mobile_footer = form.cleaned_data['our_mobile_mobile_footer']
            explore_link_footer = form.cleaned_data['explore_link_footer']
            explore_link_home_footer = form.cleaned_data['explore_link_home_footer']
            explore_link_about_footer = form.cleaned_data['explore_link_about_footer']
            explore_link_features_footer = form.cleaned_data['explore_link_features_footer']
            explore_link_contact_footer = form.cleaned_data['explore_link_contact_footer']
            explore_link_blog_footer = form.cleaned_data['explore_link_blog_footer']
            explore_link_events_footer = form.cleaned_data['explore_link_events_footer']
            explore_link_donations_footer = form.cleaned_data['explore_link_donations_footer']
            explore_link_sermons_footer = form.cleaned_data['explore_link_sermons_footer']
            explore_link_latest_post_footer = form.cleaned_data['explore_link_latest_post_footer']
            explore_link_posts_footer = form.cleaned_data['explore_link_posts_footer']
            date_footer = form.cleaned_data['date_footer']
            time_footer = form.cleaned_data['time_footer']
            day_footer = form.cleaned_data['day_footer']
            img_url_footer = form.cleaned_data['img_url_footer']
            file_footer = form.cleaned_data['file_footer']
            site_name_footer = form.cleaned_data['site_name_footer']

            # Crear el contenido del correo
            email_content = f"""
            You have received a new Footer entry:

            Title: {title_footer}
            Description: {description_footer}
            Link: {link_footer}
            Subscribe Footer: {subscribe_footer}
            Description subscribe footer: {description_subscribe_footer}
            Subscribe Button: {subscibe_boton_footer}
            The Mosque Footer: {themosque_footer}
            The Mosque Description Footer: {themosque_description_footer}
            Our Mosque Footer: {our_mosque_footer}
            Our Address Footer: {our_address_footer}
            Our Address Description Footer: {our_address_address_footer}
            Our Mobile Footer: {our_mobile_footer}
            Our Mobile Mobile Footer: {our_mobile_mobile_footer}
            Explore Link Footer: {explore_link_footer}
            Explore Link Home Footer: {explore_link_home_footer}
            Explore Link About Footer: {explore_link_about_footer}
            Explore Link Features Footer: {explore_link_features_footer}
            Explore Link Contact Footer: {explore_link_contact_footer}
            Explore Link Blog Footer: {explore_link_blog_footer}
            Explore Link Events Footer: {explore_link_events_footer}
            Explore Link Donations Footer: {explore_link_donations_footer}
            Explore Link Sermons Footer: {explore_link_sermons_footer}
            Explore Link Latest Post Footer: {explore_link_latest_post_footer}
            Explore Link Posts Footer: {explore_link_posts_footer}
            Date Footer: {date_footer}
            Time Footer: {time_footer}
            Day Footer: {day_footer}
            Image URL Footer: {img_url_footer}
            File Footer: {file_footer}
            Site Name Footer: {site_name_footer}
            """

            # Enviar el correo electrónico
            send_mail(
                f'Message from {title_footer} - {site_name_footer}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )

            # Renderizar el template con el mensaje de éxito
            return render(request, 'mosque_web_app/footer_admin.html', {'form': form, 'message': 'Footer created successfully!', 'site_name_footer': site_name_footer, 'title_footer': title_footer, 'footer1': footer1,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

    else:
        form = FooterForm()

    return render(request, 'mosque_web_app/footer_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_footer_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_footer_admin_view = Footer.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_footer_admin_view.html', {'la_lista_footer_admin_view': la_lista_footer_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_footer_admin(request, id_footer_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    footer_admin = Footer.objects.get(pk=id_footer_admin)
    form = FooterForm(request.POST or None, request.FILES or None,  instance=footer_admin)
    if form.is_valid():
        form.save()
        return redirect('list_footer_admin_view')
    context = {'footer_admin': footer_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_footer_admin.html', context)

def eliminar_footer_admin(request, id_footer_admin):
    footer_admin = get_object_or_404(Footer, id=id_footer_admin)
    footer_admin.delete()
    messages.success(request, "El Footer ha sido eliminado con éxito.")
    return redirect('list_footer_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal



def donation_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)  # Aseguramos que los archivos también se manejen
        if form.is_valid():
            # Guardar el objeto Donation en la base de datos
            donation = form.save()

            # Obtener los datos del formulario
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            amount_required = form.cleaned_data['amount_required']
            amount_collected = form.cleaned_data['amount_collected']
            is_active = form.cleaned_data['is_active']

            # Crear el contenido del correo
            email_content = f"""
            You have received a new Donation entry:

            Title: {title}
            Description: {description}
            Amount Required: {amount_required}
            Amount Collected: {amount_collected}
            Is Active: {is_active}
            """

            # Enviar el correo electrónico
            send_mail(
                f'New Donation Entry: {title}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )

            # Renderizar el template con el mensaje de éxito
            return render(request, 'mosque_web_app/donation_admin.html', {'form': form, 'message': 'Donation created successfully!', 'title': title, 'donation': donation,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

    else:
        form = DonationForm()
    
    return render(request, 'mosque_web_app/donation_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_donation_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_donation_admin_view = Donation.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_donation_admin_view.html', {'la_lista_donation_admin_view': la_lista_donation_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_donation_admin(request, id_donation_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    donation_admin = Donation.objects.get(pk=id_donation_admin)
    form = DonationForm(request.POST or None, request.FILES or None,  instance=donation_admin)
    if form.is_valid():
        form.save()
        return redirect('list_donation_admin_view')
    context = {'donation_admin': donation_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_donation_admin.html', context)

def eliminar_donation_admin(request, id_donation_admin):
    donation_admin = get_object_or_404(Donation, id=id_donation_admin)
    donation_admin.delete()
    messages.success(request, "El Donation ha sido eliminada con éxito.")
    return redirect('list_donation_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal


def post_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Aseguramos que los archivos también se manejen
        if form.is_valid():
            # Guardar el objeto Post en la base de datos
            post = form.save()

            # Obtener los datos del formulario
            title_post = form.cleaned_data['title_post']
            description_post = form.cleaned_data['description_post']
            link_post = form.cleaned_data['link_post']
            explore_link_latest_post_date_footer = form.cleaned_data['explore_link_latest_post_date_footer']
            explore_link_latest_post_time_footer = form.cleaned_data['explore_link_latest_post_time_footer']
            explore_link_latest_post_day_footer = form.cleaned_data['explore_link_latest_post_day_footer']
            image_post = form.cleaned_data['image_post']
            file_post = form.cleaned_data['file_post']

            # Crear el contenido del correo
            email_content = f"""
            You have received a new Post entry:

            Title: {title_post}
            Description: {description_post}
            Link: {link_post}
            Explore Link Latest Post Date: {explore_link_latest_post_date_footer}
            Explore Link Latest Post Time: {explore_link_latest_post_time_footer}
            Explore Link Latest Post Day: {explore_link_latest_post_day_footer}
            Image URL: {image_post}
            File URL: {file_post}
            """

            # Enviar el correo electrónico
            send_mail(
                f'New Post Entry: {title_post}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )

            # Renderizar el template con el mensaje de éxito
            return render(request, 'mosque_web_app/post_admin.html', {'form': form, 'message': 'Post created successfully!', 'title_post': title_post, 'post': post,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

    else:
        form = PostForm()

    return render(request, 'mosque_web_app/post_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})


def list_post_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_post_admin_view = Post.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_post_admin_view.html', {'la_lista_post_admin_view': la_lista_post_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_post_admin(request, id_post_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    post_admin = Post.objects.get(pk=id_post_admin)
    form = PostForm(request.POST or None, request.FILES or None,  instance=post_admin)
    if form.is_valid():
        form.save()
        return redirect('list_post_admin_view')
    context = {'post_admin': post_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_post_admin.html', context)

def eliminar_post_admin(request, id_post_admin):
    post_admin = get_object_or_404(Post, id=id_post_admin)
    post_admin.delete()
    messages.success(request, "El Post ha sido eliminado con éxito.")
    return redirect('list_post_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal



def contact_info_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, request.FILES)  # Aseguramos que los archivos también se manejen
        if form.is_valid():
            # Guardar el objeto ContactInfo en la base de datos
            contact_info = form.save()

            # Obtener los datos del formulario
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            facebook_url = form.cleaned_data['facebook_url']
            twitter_url = form.cleaned_data['twitter_url']
            linkedin_url = form.cleaned_data['linkedin_url']
            instagram_url = form.cleaned_data['instagram_url']
            date_contact_info = form.cleaned_data['date_contact_info']
            time_contact_info = form.cleaned_data['time_contact_info']
            day_contact_info = form.cleaned_data['day_contact_info']
            img_url_contact_info = form.cleaned_data['img_url_contact_info']
            file_contact_info = form.cleaned_data['file_contact_info']

            # Crear el contenido del correo
            email_content = f"""
            A new Contact Info entry has been created:

            Phone Number: {phone_number}
            Email: {email}
            Facebook URL: {facebook_url}
            Twitter URL: {twitter_url}
            LinkedIn URL: {linkedin_url}
            Instagram URL: {instagram_url}
            Date: {date_contact_info}
            Time: {time_contact_info}
            Day: {day_contact_info}
            Image URL: {img_url_contact_info}
            File URL: {file_contact_info}
            """

            # Enviar el correo electrónico
            send_mail(
                'New Contact Info Entry',  # Asunto
                email_content,  # Cuerpo del correo
                'msb.caixa@gmail.com',  # Correo del remitente
                [email, 'msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )

            # Renderizar el template con el mensaje de éxito
            return render(request, 'mosque_web_app/contact_info_admin.html', {
                'form': form,
                'message': 'Contact Info created successfully!',
                'phone_number': phone_number,
                'contact_info': contact_info,'donations': donations,
                'posts': posts,
                'footer': footer,
                'footer_subscribe_footer': footer_subscribe_footer,
                'footer_description_subscribe_footer': footer_description_subscribe_footer,
                'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
                'footer_themosque_footer': footer_themosque_footer,
                'footer_link_footer': footer_link_footer,
                'footer_our_mosque_footer': footer_our_mosque_footer,
                'footer_our_address_footer': footer_our_address_footer,
                'footer_our_mobile_footer': footer_our_mobile_footer,
                'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
                'footer_site_name_footer': footer_site_name_footer,
                'contact_info': contact_info,
                'page': page,
                'tabs': tabs,
                'tab_pages': tab_pages,
            })

    else:
        form = ContactInfoForm()

    return render(request, 'mosque_web_app/contact_info_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def list_contact_info_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_contact_info_admin_view = ContactInfo.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_contact_info_admin_view.html', {'la_lista_contact_info_admin_view': la_lista_contact_info_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_contact_info_admin(request, id_contact_info_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    contact_info_admin = ContactInfo.objects.get(pk=id_contact_info_admin)
    form = ContactInfoForm(request.POST or None, request.FILES or None,  instance=contact_info_admin)
    if form.is_valid():
        form.save()
        return redirect('list_contact_info_admin_view')
    context = {'contact_info_admin': contact_info_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_contact_info_admin.html', context)

def eliminar_contact_info_admin(request, id_contact_info_admin):
    contact_info_admin = get_object_or_404(ContactInfo, id=id_contact_info_admin)
    contact_info_admin.delete()
    messages.success(request, "El contact info admin ha sido eliminado con éxito.")
    return redirect('list_contact_info_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal



def page_admin(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)  # Aseguramos que los archivos también se manejen
        if form.is_valid():
            # Guardar el objeto Page en la base de datos
            page1 = form.save()

            # Obtener los datos del formulario
            title = form.cleaned_data['title']
            url_name = form.cleaned_data['url_name']
            is_dropdown = form.cleaned_data['is_dropdown']
            parent = form.cleaned_data['parent']
            welcome_to_the_mosque = form.cleaned_data['welcome_to_the_mosque']
            purity_comes_from_faith = form.cleaned_data['purity_comes_from_faith']
            date_page = form.cleaned_data['date_page']
            time_page = form.cleaned_data['time_page']
            day_page = form.cleaned_data['day_page']
            img_url_page = form.cleaned_data['img_url_page']
            file_page = form.cleaned_data['file_page']

            # Crear el contenido del correo
            email_content = f"""
            A new Page entry has been created:

            Title: {title}
            URL Name: {url_name}
            Is Dropdown: {is_dropdown}
            Parent: {parent}
            Welcome Message: {welcome_to_the_mosque}
            Purity Comes From Faith: {purity_comes_from_faith}
            Date: {date_page}
            Time: {time_page}
            Day: {day_page}
            Image URL: {img_url_page}
            File URL: {file_page}
            """

            # Enviar el correo electrónico
            send_mail(
                f'New Page Entry: {title}',  # Asunto
                email_content,  # Cuerpo del correo
                'msb.caixa@gmail.com',  # Correo del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )

            # Renderizar el template con el mensaje de éxito
            return render(request, 'mosque_web_app/page_admin.html', {
                'form': form,
                'message': 'Page created successfully!',
                'title': title,
                'page1': page1,'donations': donations,
                'posts': posts,
                'footer': footer,
                'footer_subscribe_footer': footer_subscribe_footer,
                'footer_description_subscribe_footer': footer_description_subscribe_footer,
                'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
                'footer_themosque_footer': footer_themosque_footer,
                'footer_link_footer': footer_link_footer,
                'footer_our_mosque_footer': footer_our_mosque_footer,
                'footer_our_address_footer': footer_our_address_footer,
                'footer_our_mobile_footer': footer_our_mobile_footer,
                'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
                'footer_site_name_footer': footer_site_name_footer,
                'contact_info': contact_info,
                'page': page,
                'tabs': tabs,
                'tab_pages': tab_pages,
            })
    
    else:
        form = PageForm()

    return render(request, 'mosque_web_app/page_admin.html', {'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})


def list_page_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_page_admin_view = Page.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_page_admin_view.html', {'la_lista_page_admin_view': la_lista_page_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,})

def actualizar_page_admin(request, id_page_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    page_admin = Page.objects.get(pk=id_page_admin)
    form = PageForm(request.POST or None, request.FILES or None,  instance=page_admin)
    if form.is_valid():
        form.save()
        return redirect('list_page_admin_view')
    context = {'page_admin': page_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_page_admin.html', context)

def eliminar_page_admin(request, id_page_admin):
    page_admin = get_object_or_404(Page, id=id_page_admin)
    page_admin.delete()
    messages.success(request, "El page admin ha sido eliminado con éxito.")
    return redirect('list_page_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal

@cache_page(0)  # Desactiva la caché
def best_videos(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    #bestVideos  = BestVideos.objects.all() if BestVideos.objects.exists() else None
    bestVideos = BestVideos.objects.filter(is_active=True)
    
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    context = {'form': '','donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'bestVideos': bestVideos,
        'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/best_videos.html',context )




def best_videos_admin(request):
    # Obtener la página principal activa (si existe)
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    # Obtener la información de contacto activa (si existe)
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los videos destacados (si existen)
    best_videos = BestVideos.objects.filter(is_active=True) if BestVideos.objects.exists() else None
    
    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None
    
    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    if request.method == 'POST':
        form = BestVideosForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el video en la base de datos
            form.save()
            
            # Obtener los datos del formulario
            video_ref = form.cleaned_data['best_video_ref']
            video_name = form.cleaned_data['best_video_name']
            video_description = form.cleaned_data['best_video_description']
            best_video_url = form.cleaned_data['best_video_url']
            best_video_img_url = form.cleaned_data['best_video_img_url']
            best_video_file = form.cleaned_data['best_video_file']
            
            # Preparar el contenido para el correo electrónico
            email_content = f"""
            You have received a new Best Video submission:
            
            Video Reference: {video_ref}
            Video Name: {video_name}
            Description: {video_description}
            best_video_url: {best_video_url}
            best_video_img_url: {best_video_img_url}
            best_video_file: {best_video_file}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'New Best Video: {video_name}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            
            return render(request, 'mosque_web_app/best_videos_admin.html', {
                'video_ref': video_ref,
                'video_name': video_name,
                'video_description': video_description,
                'donations': donations,
                'posts': posts,
                'footer': footer,
                'footer_subscribe_footer': footer_subscribe_footer,
                'footer_description_subscribe_footer': footer_description_subscribe_footer,
                'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
                'footer_themosque_footer': footer_themosque_footer,
                'footer_link_footer': footer_link_footer,
                'footer_our_mosque_footer': footer_our_mosque_footer,
                'footer_our_address_footer': footer_our_address_footer,
                'footer_our_mobile_footer': footer_our_mobile_footer,
                'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
                'footer_site_name_footer': footer_site_name_footer,
                'contact_info': contact_info,
                'page': page,
                'tabs': tabs,
                'tab_pages': tab_pages,
            })
    else:
        form = BestVideosForm()

    return render(request, 'mosque_web_app/best_videos_admin.html', {
        'form': form,
        'best_videos': best_videos,
        'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,
    })


def list_best_videos_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    la_lista_best_videos_admin_view = BestVideos.objects.all()  # Recupera todos los servicios
    return render(request, 'mosque_web_app/list_best_videos_admin_view.html', {'la_lista_best_videos_admin_view': la_lista_best_videos_admin_view,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,'tabs': tabs,
        'tab_pages': tab_pages,})


def actualizar_best_videos_admin(request, id_best_videos_admin):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    best_videos_admin = BestVideos.objects.get(pk=id_best_videos_admin)
    form = BestVideosForm(request.POST or None, request.FILES or None,  instance=best_videos_admin)
    if form.is_valid():
        form.save()
        return redirect('list_best_videos_admin_view')
    context = {'best_videos_admin': best_videos_admin, 'form': form,'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,'tabs': tabs,
        'tab_pages': tab_pages,}
    return render(request, 'mosque_web_app/actualizar_best_videos_admin.html', context)

def eliminar_best_videos_admin(request, id_best_videos_admin):
    best_videos_admin = get_object_or_404(BestVideos, id=id_best_videos_admin)
    best_videos_admin.delete()
    messages.success(request, "El best videos admin ha sido eliminado con éxito.")
    return redirect('list_best_videos_admin_view')  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista principal


def tab_admin(request):
    # Obtener la página principal activa (si existe)
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    # Obtener la información de contacto activa (si existe)
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los videos destacados (si existen)
    best_videos = BestVideos.objects.filter(is_active=True) if BestVideos.objects.exists() else None
    
    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None
    
    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    if request.method == 'POST':
        form = TabForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el video en la base de datos
            form.save()
            
            # Obtener los datos del formulario
            tab_slug = form.cleaned_data['tab_slug']
            tab_nombre = form.cleaned_data['tab_nombre']
            tab_description = form.cleaned_data['tab_description']
            tab_url = form.cleaned_data['tab_url']
            tab_img_url = form.cleaned_data['tab_img_url']
            tab_file = form.cleaned_data['tab_file']
            tab_date_page = form.cleaned_data['tab_date_page']
            tab_time_page = form.cleaned_data['tab_time_page']
            tab_day_page = form.cleaned_data['tab_day_page']
            is_active = form.cleaned_data['is_active']
            
            # Preparar el contenido para el correo electrónico
            email_content = f"""
            You have received a new Tab submission:
            
            tab_slug: {tab_slug}
            tab_nombre: {tab_nombre}
            tab_description: {tab_description}
            tab_url: {tab_url}
            tab_img_url: {tab_img_url}
            tab_file: {tab_file}
            tab_date_page: {tab_date_page}
            tab_time_page: {tab_time_page}
            tab_day_page: {tab_day_page}
            is_active: {is_active}
            """
            
            # Enviar el correo electrónico
            send_mail(
                f'New Tab: {tab_nombre}',  # Asunto
                email_content,  # Cuerpo del correo con todos los detalles
                'msb.caixa@gmail.com',  # Correo electrónico del remitente
                ['msb.caixa@gmail.com','msb.tesla@gmail.com', 'msb.coin@gmail.com', 'msb.duck@gmail.com', 'msebti2@gmail.com', 'papioles@gmail.com', 'msb.motive@gmail.com', 'msb.acer@gmail.com'],  # Correos de destino
            )
            
            return render(request, 'mosque_web_app/tab_admin.html', {
                'tab_slug': tab_slug,
                'tab_nombre': tab_nombre,
                'tab_description': tab_description,
                'donations': donations,
                'posts': posts,
                'footer': footer,
                'footer_subscribe_footer': footer_subscribe_footer,
                'footer_description_subscribe_footer': footer_description_subscribe_footer,
                'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
                'footer_themosque_footer': footer_themosque_footer,
                'footer_link_footer': footer_link_footer,
                'footer_our_mosque_footer': footer_our_mosque_footer,
                'footer_our_address_footer': footer_our_address_footer,
                'footer_our_mobile_footer': footer_our_mobile_footer,
                'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
                'footer_site_name_footer': footer_site_name_footer,
                'contact_info': contact_info,
                'page': page,
                'tabs': tabs,
                'tab_pages': tab_pages,
            })
    else:
        form = TabForm()
    
    return render(request, 'mosque_web_app/tab_admin.html', {
        'form': form,
        'best_videos': best_videos,
        'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'tabs': tabs,
        'tab_pages': tab_pages,
    })











def mosque_web_admin_view(request):
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None

    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    context = {'form': '','donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,'tabs': tabs,
        'tab_pages': tab_pages,}
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
    
    page = (
        Page.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if Page.objects.exists() else None
    )
    
    contact_info = (
        ContactInfo.objects.filter(is_active=True)
        .order_by('-updated_at', '-created_at')
        .first() if ContactInfo.objects.exists() else None
    )
    
    tabs = Tab.objects.filter(is_active=True)  # Solo pestañas activas
    
    tab_pages = TabPage.objects.all()
    
    # Obtener el último footer (si existe)
    footer = Footer.objects.latest('created_at') if Footer.objects.exists() else None
    
    
    testimonials = Testimonial.objects.all() if Testimonial.objects.exists() else None


    last_activity = Activity.objects.order_by('-id').first() if Activity.objects.exists() else None
    
    # Obtener todos los posts (si existen)
    posts = Post.objects.all() if Post.objects.exists() else None

    # Obtener todas las donaciones (si existen)
    donations = Donation.objects.all() if Donation.objects.exists() else None
    
    events = Event.objects.all() if Event.objects.exists() else None
    
    sermons  = Sermon.objects.all() if Sermon.objects.exists() else None
    
    blogs = Blog.objects.all().order_by('-date_blog', '-time_blog') if Blog.objects.exists() else None
    
    testimonials  = Testimonial.objects.all().order_by('-testimonial_date', '-testimonial_time') if Testimonial.objects.exists() else None
    
    # Variables para pasar al template
    footer_subscribe_footer = footer.subscribe_footer if footer else 'No footer available'
    footer_description_subscribe_footer = footer.description_subscribe_footer if footer else 'No description available.'
    footer_subscibe_boton_footer = footer.subscibe_boton_footer if footer else 'Subscribe'
    footer_themosque_footer = footer.themosque_footer if footer else 'No footer description.'
    footer_link_footer = footer.link_footer if footer else '#'
    footer_our_mosque_footer = footer.our_mosque_footer if footer else 'No mosque info.'
    footer_our_address_footer = footer.our_address_footer if footer else 'No address.'
    footer_our_mobile_footer = footer.our_mobile_footer if footer else 'No mobile info.'
    footer_our_mobile_mobile_footer = footer.our_mobile_mobile_footer if footer else 'No phone info.'
    footer_site_name_footer = footer.site_name_footer if footer else 'Website'
    
    abouts_images = AboutImages.objects.all()
    team_members = TeamMember.objects.all()
    for member in team_members:
        if member.team_social_links:
            # Asegúrate de que sea un diccionario válido
            if isinstance(member.team_social_links, str):
                try:
                    member.team_social_links = json.loads(member.team_social_links)
                except json.JSONDecodeError:
                    member.team_social_links = {}
            elif not isinstance(member.team_social_links, dict):
                member.team_social_links = {}
        else:
            member.team_social_links = {}
    president = TeamMember.objects.filter(team_position="President").first()  # Obtén el presidente (si existe)
    other_members = TeamMember.objects.exclude(team_position="President")  # Excluye al presidente
 
    try:
        about = About.objects.latest('id')  # Obtiene el último registro basado en el campo 'id'
    except About.DoesNotExist:
        about = None  # Maneja el caso donde no hay registros en la base de datos
    
    context = {
        'fecha_actual': fecha_actual,
        'fecha_actual_es': fecha_actual_es,
        'fecha_hora_actual': fecha_hora_actual,
        'donations': donations,
        'posts': posts,
        'footer': footer,
        'footer_subscribe_footer': footer_subscribe_footer,
        'footer_description_subscribe_footer': footer_description_subscribe_footer,
        'footer_subscibe_boton_footer': footer_subscibe_boton_footer,
        'footer_themosque_footer': footer_themosque_footer,
        'footer_link_footer': footer_link_footer,
        'footer_our_mosque_footer': footer_our_mosque_footer,
        'footer_our_address_footer': footer_our_address_footer,
        'footer_our_mobile_footer': footer_our_mobile_footer,
        'footer_our_mobile_mobile_footer': footer_our_mobile_mobile_footer,
        'footer_site_name_footer': footer_site_name_footer,
        'contact_info': contact_info,
        'page': page,
        'about': about, 'abouts_images': abouts_images, 'team_members': team_members, 'president': president,
        'other_members': other_members, 'testimonials': testimonials, 'last_activity': last_activity, 'events': events, 'sermons': sermons, 'blogs': blogs,'tabs': tabs,'tab_pages': tab_pages,
    }
    return render(request, 'mosque_web_app/home.html', context)