from django.contrib import admin

from .models import PDF, Publication_user, advertisement  # Ensure the correct import path

admin.site.register(PDF)
admin.site.register(Publication_user)
admin.site.register(advertisement)
