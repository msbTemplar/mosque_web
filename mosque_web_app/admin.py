from django.contrib import admin
from .models import ContactMessage,About,Activity,Event,Error404,Sermon,Blog,TeamMember,Testimonial,Newsletter
# Register your models here.

#admin.site.register(ContactMessage)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','message', 'created_at')
    readonly_fields = ('created_at',)
admin.site.register(About)
admin.site.register(Activity)
admin.site.register(Event)
admin.site.register(Error404)
admin.site.register(Sermon)
admin.site.register(Blog)
admin.site.register(TeamMember)
admin.site.register(Testimonial)
admin.site.register(Newsletter)