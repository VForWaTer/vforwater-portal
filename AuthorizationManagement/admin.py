from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import *

admin.site.register(Resource)
admin.site.register(AccessRequest)
admin.site.register(DeletionRequest)
 
#this is the subpage 'Manage Resources' only displayable to the admin
class ResourceManager(AdminSite):      
    pass
    #or methods         
resource_manager = AdminSite(name="ResourceManager")

class ResourceAdmin(admin.ModelAdmin):
    list_display = ["name", 
                    "type", 
                    "description"]
    search_fields = ["name", 
                     "type", 
                     "description"]
    
resource_manager.register(Resource, ResourceAdmin)
# Text to put at the end of each page's <title>.
resource_manager.site_title = 'Site Admin'

# Text to put in each page's <h1> (and above login form).
resource_manager.site_header = 'Resources Manager'

# Text to put at the top of the admin index page.
resource_manager.index_title = 'Administration'


#this is the subpage 'Manage Users' also only displayable to the admin
class UserManager(AdminSite):
    pass
    #or methods    
user_manager = AdminSite(name="UserManager")

class UserAdmin(admin.ModelAdmin):
    list_display = ["username",
                    "last_name", 
                    "first_name", 
                    "email", 
                    "is_active", 
                    "is_staff", 
                    "last_login", 
                    "date_joined"]
    search_fields = ["username" , 
                     "email", 
                     "first_name", 
                     "last_name"]
    
user_manager.register(User, UserAdmin)
# Text to put at the end of each page's <title>.
user_manager.site_title = 'Site Admin'

# Text to put in each page's <h1> (and above login form).
user_manager.site_header = 'Users Manager'

# Text to put at the top of the admin index page.
user_manager.index_title = 'Administration'
    