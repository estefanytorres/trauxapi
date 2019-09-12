from django.contrib import admin
from api.models import (
    MessageSet,
    MessageCatalog,
    Client,
    Module,
    License,
    UserProfile
)

# Register your models here.
admin.site.register(MessageSet)
admin.site.register(MessageCatalog)
admin.site.register(UserProfile)
admin.site.register(Client)
admin.site.register(Module)
admin.site.register(License)