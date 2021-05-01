from django.contrib import admin
from .models import *
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user','role')
  pass
  
admin.site.register(UserProfileModel,UserProfileAdmin)

#class DonationAdmin(admin.ModelAdmin):
#  list_display = ('nama','nilai')
#  pass
  
#admin.site.register(DonationModel,DonationAdmin)

class SubscribeAdmin(admin.ModelAdmin):
  list_display = ('email', 'waktu_subscribe')
  pass
  
admin.site.register(SubscriberModel,SubscribeAdmin)

class ProjectDetailAdmin(admin.ModelAdmin):
  list_display = ('project_id', 'user_id')
  pass
admin.site.register(ProjectDetailModel,ProjectDetailAdmin)