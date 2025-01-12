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