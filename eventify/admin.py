from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(OrganizerProfile)
admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Ticket)
admin.site.register(Review)


admin.site.index_title = "Eventify Admin"
admin.site.site_header = "Eventify Admin Panel"
admin.site.site_title = "Eventify Admin Panel"
