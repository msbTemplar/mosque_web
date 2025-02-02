from django.contrib import admin
from .models import ContactMessage,About,Activity,Event,Error404,Sermon,Blog,TeamMember,Testimonial,Newsletter,AboutImages, Footer, Post, Donation, Page, ContactInfo, BestVideos, Tab, TabPage
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
admin.site.register(Footer)
admin.site.register(Post)
admin.site.register(Donation)
admin.site.register(Page)
admin.site.register(ContactInfo)
admin.site.register(BestVideos)
admin.site.register(Tab)
admin.site.register(TabPage)
#admin.site.register(AboutImages)

@admin.register(AboutImages)
class AboutImagesAdmin(admin.ModelAdmin):
    list_display = ('about_images_the_about_image', 'img_url_about_images', 'created_at')
    readonly_fields = ('created_at',)