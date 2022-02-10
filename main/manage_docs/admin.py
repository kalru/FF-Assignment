from django.contrib import admin
from .models import RelationshipManager, Client, Document

admin.site.register(RelationshipManager)
admin.site.register(Client)
admin.site.register(Document)
