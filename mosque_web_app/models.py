from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.
class Newsletter(models.Model):
    email = models.EmailField(unique=True)  # Almacenará el correo electrónico
    date_subscribed = models.DateTimeField(auto_now_add=True)  # Fecha de suscripción
    is_active = models.BooleanField(default=True)  # Permitir activar o desactivar la suscripción
    
    def __str__(self):
        return self.email
    
    
class Testimonial(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    user_creator_testimonial = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="testimonials"
    )
    testimonial_full_name = models.CharField(max_length=500, blank=True, null=True)
    testimonial_position = models.CharField(max_length=500, blank=True, null=True)
    testimonial_status = models.CharField(max_length=500, blank=True, null=True)
    testimonial_description = models.TextField(blank=True, null=True)
    testimonial_date_of_birth = models.DateField(blank=True, null=True)
    testimonial_email = models.EmailField(blank=True, null=True)
    testimonial_phone_number = models.CharField(max_length=15, blank=True, null=True)
    testimonial_link = models.URLField(max_length=4500, blank=True, null=True)
    testimonial_img_url = models.ImageField(upload_to='testimonial_images/', max_length=5500, blank=True, null=True)
    testimonial_date = models.DateField(blank=True, null=True)
    testimonial_time = models.TimeField(blank=True, null=True)
    testimonial_day = models.CharField(max_length=9, choices=DAYS_OF_WEEK, blank=True, null=True)
    testimonial_social_links = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.testimonial_full_name} - {self.testimonial_position}'

    

class TeamMember(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    user_creator_team_member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams")
    team_full_name = models.CharField(max_length=500)
    team_position = models.CharField(max_length=500, blank=True, null=True)  # Posición en el equipo
    team_status = models.CharField(max_length=500)
    team_life_situation = models.CharField(max_length=500)
    team_description = models.TextField()
    team_date_of_birth = models.DateField()  # Cambiado a DateField para solo la fecha
    team_email = models.EmailField()
    team_address = models.TextField()  # Corregí `team_addresse` a `team_address`
    team_phone_number = models.CharField(max_length=15)  # Máximo estándar para números internacionales
    team_link = models.URLField(max_length=4500, blank=True, null=True)
    team_img_url = models.ImageField(upload_to='team_images/', max_length=5500, blank=True, null=True, default='path/to/default/image.jpg')
    team_date_start = models.DateField()
    team_time_start = models.TimeField()
    team_day_start = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    team_social_links = models.JSONField(blank=True, null=True)  # Opcional para enlaces sociales

    def __str__(self):
        return f'{self.team_full_name} - {self.team_status}'
    
    

class Blog(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    user_blog = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")  # Relación con el usuario
    blog_title = models.CharField(max_length=500)
    description_blog = models.TextField()
    link_blog = models.URLField(max_length=4500,blank=True, null=True)
    img_url_blog = models.ImageField(upload_to='sermons_images/', max_length=5500, blank=True, null=True)
    date_blog = models.DateField()
    time_blog = models.TimeField()
    day_blog = models.CharField(max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    number_coments_blog= models.DecimalField('Number Comments Blog', max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Message from {self.blog_title} - {self.description_blog}'

class Sermon(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    user_sermon = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sermons")  # Relación con el usuario
    sermon_title = models.CharField(max_length=500)
    description_sermon = models.TextField()
    link_sermon = models.URLField(max_length=4500,blank=True, null=True)
    img_url_sermon = models.ImageField(upload_to='sermons_images/', max_length=5500, blank=True, null=True)
    date_sermon = models.DateField()
    time_sermon = models.TimeField()
    day_sermon = models.CharField(max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    file_sermon = models.FileField(upload_to='sermons_files/', max_length=5500, blank=True, null=True)  # Para subir archivos
    
    
    
    def __str__(self):
        return f'Message from {self.user_sermon} - {self.sermon_title}'

class Error404(models.Model):
    error = models.CharField(max_length=100)
    error_title = models.CharField(max_length=555)
    error_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Message from {self.error} - {self.error_title}'

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Message from {self.name} - {self.subject}'
    
    

class About(models.Model):
    about_the_mosque = models.CharField(max_length=500)
    allah_helps_those = models.CharField(max_length=1000)
    description_about = models.TextField()
    our_vision = models.CharField(max_length=500)
    description_our_vision = models.TextField()
    our_mission = models.CharField(max_length=500)
    description_our_mission = models.TextField()
    raised = models.CharField(max_length=500)
    raised_value = models.CharField(max_length=500)
    description_raised = models.TextField()
    img_url_raised_about = models.ImageField(upload_to='about_raised_images/', max_length=5500, blank=True, null=True)
    charity_and_donation = models.CharField(max_length=500)
    parent_education = models.CharField(max_length=500)
    hadith_and_sunnah = models.CharField(max_length=500)
    mosque_development = models.CharField(max_length=500)
    file_about = models.FileField(upload_to='abouts_files/', max_length=5500, blank=True, null=True)  # Para subir 
    
    def __str__(self):
        return f'{self.about_the_mosque} - {self.allah_helps_those}'
    
class AboutImages(models.Model):
    about_images_the_about_image = models.CharField(max_length=500)
    img_url_about_images = models.ImageField(upload_to='about_images_images/', max_length=5500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.about_images_the_about_image} - {self.created_at}'
    
class Activity(models.Model):
    activity_title = models.CharField(max_length=500)
    activity_mosque_development = models.CharField(max_length=500)
    description_activity_mosque_development = models.TextField()
    activity_charity_donation = models.CharField(max_length=500)
    description_activity_charity_donation = models.TextField()
    activity_quran_learning = models.CharField(max_length=500)
    description_activity_quran_learning = models.TextField()
    activity_hadith_sunnah = models.CharField(max_length=500)
    description_activity_hadith_sunnah = models.TextField()
    activity_parent_education = models.CharField(max_length=500)
    description_activity_parent_education = models.TextField()
    activity_help_orphans = models.CharField(max_length=500)
    description_activity_help_orphans = models.TextField()
    activity_testimonial = models.CharField(max_length=500)
    activity_title_testimonial = models.CharField(max_length=500)
    
    def __str__(self):
        return f'{self.activity_title} - {self.activity_mosque_development}'

class Event(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    title_event = models.CharField(max_length=500)
    description_title_event = models.TextField()
    link_event = models.URLField(max_length=4500,blank=True, null=True)
    img_url_event = models.ImageField(upload_to='events_images/', max_length=5500, blank=True, null=True)
    date_event = models.DateField()
    time_event = models.TimeField()
    day_event = models.CharField(max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    file_event = models.FileField(upload_to='events_files/', max_length=5500, blank=True, null=True)  # Para subir archivos
    
    def __str__(self):
        return self.title_event
    
class Donation(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, help_text="Título para la donación (ej: 'Ayuda para el Orfanato')")
    description = models.TextField(blank=True, null=True, help_text="Descripción breve de la donación.")
    amount_required = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Monto total requerido para esta donación.", blank=True, null=True
    )
    amount_collected = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        help_text="Monto que ya ha sido recaudado.", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha en la que se creó la donación.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última vez que se actualizó esta donación.")
    is_active = models.BooleanField(default=True, help_text="Define si esta donación está activa y visible.")

    def __str__(self):
        return f"{self.title} - ${self.amount_collected} / ${self.amount_required}"

    def percentage_collected(self):
        """Calcula el porcentaje de donaciones recaudadas."""
        if self.amount_required > 0:
            return (self.amount_collected / self.amount_required) * 100
        return 0

class Post(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    title_post = models.CharField(max_length=200,blank=True, null=True, help_text="Título del post")
    description_post = models.TextField(blank=True, null=True, help_text="Descripción del post.")
    link_post = models.URLField(max_length=4500,blank=True, null=True, help_text="Enlace al post completo")
    explore_link_latest_post_date_footer = models.DateField(help_text="Fecha de publicación",blank=True, null=True)
    explore_link_latest_post_time_footer = models.TimeField(help_text="Hora de publicación",blank=True, null=True)
    explore_link_latest_post_day_footer = models.CharField(help_text="Dia de publicación", max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    image_post = models.ImageField(upload_to='latest_posts/', help_text="Imagen del post", max_length=5500, blank=True, null=True)
    file_post = models.FileField(upload_to='posts_files/', help_text="File del post" , max_length=5500, blank=True, null=True)  #
    
    def __str__(self):
        return self.title_post
       
class Footer(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    subscribe_footer = models.CharField(help_text="Subscribe_footer", max_length=500,blank=True, null=True)
    description_subscribe_footer = models.TextField(blank=True, null=True)
    subscibe_boton_footer = models.CharField(max_length=500, blank=True, null=True)
    themosque_footer = models.TextField(blank=True, null=True)
    themosque_description_footer = models.TextField(blank=True, null=True)
    our_mosque_footer = models.CharField(max_length=500, blank=True, null=True)
    our_address_footer = models.CharField(max_length=500, blank=True, null=True)
    our_address_address_footer = models.TextField(blank=True, null=True)
    our_mobile_footer = models.CharField(max_length=500, blank=True, null=True)
    our_mobile_mobile_footer = models.CharField(max_length=500, blank=True, null=True)
    explore_link_footer = models.CharField(max_length=500, blank=True, null=True)
    #explore_link_home_footer = models.ForeignKey(Home, blank=True, null=True, on_delete=models.CASCADE)
    explore_link_home_footer = models.CharField(max_length=500, blank=True, null=True)
    explore_link_about_footer = models.ForeignKey(About, blank=True, null=True, on_delete=models.CASCADE)
    explore_link_features_footer = models.ForeignKey(Activity, blank=True, null=True, on_delete=models.CASCADE)
    explore_link_contact_footer = models.ForeignKey(ContactMessage, blank=True, null=True, on_delete=models.CASCADE)
    explore_link_blog_footer = models.ForeignKey(Blog, blank=True, null=True, on_delete=models.CASCADE)
    explore_link_events_footer = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)
    explore_link_donations_footer = models.ForeignKey(Donation, blank=True, null=True, on_delete=models.CASCADE)
    explore_link_sermons_footer = models.ForeignKey(Sermon, blank=True, null=True, on_delete=models.CASCADE)
    
    explore_link_posts_footer = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    explore_link_latest_post_footer = models.CharField(max_length=500, blank=True, null=True)
    date_footer = models.DateField(help_text="Fecha de footer", blank=True, null=True)
    time_footer = models.TimeField(help_text="Hora de footer", blank=True, null=True)
    day_footer = models.CharField(max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    description_footer = models.TextField()
    title_footer = models.CharField(max_length=500,blank=True, null=True, help_text="Título del Footer")
    link_footer = models.URLField(max_length=4500,blank=True, null=True)
    img_url_footer = models.ImageField(upload_to='footer_images/', max_length=5500, blank=True, null=True)
    file_footer = models.FileField(upload_to='footer_files/', max_length=5500, blank=True, null=True)  # Para subir archivos
    site_name_footer = models.CharField(help_text="Site name", max_length=500,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha en la que se creó el footer.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última vez que se actualizó el footer.")
    is_active = models.BooleanField(default=True, help_text="Define si este footer está activo y visible.")
    
    def __str__(self):
        return f'{self.title_footer} - {self.site_name_footer}'
    


class ContactInfo(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(verbose_name="Email")
    facebook_url = models.URLField(blank=True, null=True, verbose_name="Facebook URL")
    twitter_url = models.URLField(blank=True, null=True, verbose_name="Twitter URL")
    linkedin_url = models.URLField(blank=True, null=True, verbose_name="LinkedIn URL")
    instagram_url = models.URLField(blank=True, null=True, verbose_name="Instagram URL")
    
    date_contact_info = models.DateField(help_text="Fecha de footer", blank=True, null=True)
    time_contact_info = models.TimeField(help_text="Hora de footer", blank=True, null=True)
    day_contact_info = models.CharField(max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    img_url_contact_info = models.ImageField(upload_to='footer_images/', max_length=5500, blank=True, null=True)
    file_contact_info = models.FileField(upload_to='footer_files/', max_length=5500, blank=True, null=True)  # Para subir archivos
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha en la que se creó el ContactInfo.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última vez que se actualizó el ContactInfo.")
    is_active = models.BooleanField(default=True, help_text="Define si este ContactInfo está activo y visible.")

    def __str__(self):
        return f"Contact Info ({self.phone_number}, {self.email})"


class Page(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    title = models.CharField(max_length=100, verbose_name="Page Title", blank=True, null=True)
    url_name = models.CharField(max_length=100, verbose_name="URL Name", blank=True, null=True)
    is_dropdown = models.BooleanField(default=False, verbose_name="Is Dropdown", blank=True, null=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name="subpages", 
        verbose_name="Parent Page"
    )
    welcome_to_the_mosque = models.CharField(verbose_name="Welcome to the mosque", help_text="Welcome to the mosque", max_length=500,blank=True, null=True)
    
    purity_comes_from_faith = models.TextField(verbose_name="Purity comes from faith", help_text="Purity comes from faith", blank=True, null=True)
    
    date_page = models.DateField(help_text="Fecha de footer", blank=True, null=True)
    time_page = models.TimeField(help_text="Hora de footer", blank=True, null=True)
    day_page = models.CharField(max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    img_url_page = models.ImageField(upload_to='footer_images/', max_length=5500, blank=True, null=True)
    file_page = models.FileField(upload_to='footer_files/', max_length=5500, blank=True, null=True)  # Para subir archivos
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha en la que se creó el Home.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última vez que se actualizó el Home.")
    is_active = models.BooleanField(default=True, help_text="Define si este Home está activo y visible.")

    def __str__(self):
        return self.title


class BestVideos(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    best_video_ref = models.CharField(max_length=500)
    best_video_name = models.CharField(max_length=1000)
    best_video_description = models.TextField()
    best_video_url = models.URLField(blank=True, null=True, verbose_name="Best videos URL")
    best_video_img_url = models.ImageField(upload_to='best_video_img_url_images/', max_length=5500, blank=True, null=True)
    best_video_file = models.FileField(upload_to='best_video_file_files/', max_length=5500, blank=True, null=True)  # Para subir
    date_page = models.DateField(help_text="Fecha de BestVideos", blank=True, null=True)
    time_page = models.TimeField(help_text="Hora de BestVideos", blank=True, null=True)
    day_page = models.CharField(max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha en la que se creó el BestVideos.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última vez que se actualizó el BestVideos.")
    is_active = models.BooleanField(default=True, help_text="Define si este BestVideos está activo y visible.")
    
    def __str__(self):
        return f'{self.best_video_ref} - {self.best_video_name}'
    

class Tab(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    tab_slug = models.SlugField(unique=True, help_text="Identificador único de la pestaña (ej: home, about, event)")
    tab_nombre = models.CharField(max_length=100)
    tab_description = models.TextField()
    tab_url = models.URLField(blank=True, null=True, verbose_name="tab URL")
    tab_img_url = models.ImageField(upload_to='tab_img_url_images/', max_length=5500, blank=True, null=True)
    tab_file = models.FileField(upload_to='tab_file_files/', max_length=5500, blank=True, null=True)  # Para subir
    tab_date_page = models.DateField(help_text="Fecha de tab", blank=True, null=True)
    tab_time_page = models.TimeField(help_text="Hora de tab", blank=True, null=True)
    tab_day_page = models.CharField(max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha en la que se creó el tab.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última vez que se actualizó el tab.")
    is_active = models.BooleanField(default=True, help_text="Define si este tab está activo y visible.")
    
    def __str__(self):
        return f'{self.tab_nombre} - {self.tab_description}'
    

class TabPage(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    tab_page = models.ForeignKey(Tab, on_delete=models.CASCADE)
    tab_page_name = models.CharField(max_length=100, blank=True, null=True , verbose_name="tab page name")
    tab_page_url_name = models.CharField(max_length=100, blank=True, null=True , verbose_name="tab page URL name")
    tab_img_url = models.ImageField(upload_to='tab_page_img_url_images/', max_length=5500, blank=True, null=True)
    tab_file = models.FileField(upload_to='tab_page_file_files/', max_length=5500, blank=True, null=True)  # Para subir
    tab_date_page = models.DateField(help_text="Fecha de tab page", blank=True, null=True)
    tab_time_page = models.TimeField(help_text="Hora de tab page", blank=True, null=True)
    tab_day_page = models.CharField(max_length=9, choices=DAYS_OF_WEEK)  # Día seleccionado del combo
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha en la que se creó el tab page.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Última vez que se actualizó el tab page.")
    is_active = models.BooleanField(default=True, help_text="Define si este tab page está activo y visible.")

    def __str__(self):
        return self.tab_page_name
