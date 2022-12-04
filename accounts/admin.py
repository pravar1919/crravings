from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Buyer, Vendor, ObjectViewed

class CustomUserAdmin(UserAdmin):

    list_display = ('email', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email','password', 'first_name', 
                'last_name', 'mob_number', 'gst_number','pan_number', 
                'address', 'is_active', 'is_staff', 'is_buyer', 'is_vendor')}),

        ('Permissions', {'fields': ('is_superuser',)}),
    )

    search_fields =  ('email',)
    ordering = ('email',)

    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)
admin.site.register(Buyer, CustomUserAdmin)
admin.site.register(Vendor, CustomUserAdmin)

@admin.register(ObjectViewed)
class ObjectViewedAdmin(admin.ModelAdmin):
    menu_group = "Users"
    menu_title = "Users activity"
    list_display = ('user','object_id','content_type', 'model_name','model_product_id','path','timestamp')
    fields = ('user','content_type','object_id','path', 'model_name', 'model_product_id','content_object','timestamp')
    readonly_fields = ('user','content_type','object_id','path', 'model_name', 'model_product_id','content_object','timestamp')
    search_fields = ('user__email__icontains',)




