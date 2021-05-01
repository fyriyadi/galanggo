from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import *

#ModelAdmin dan ModelAdminGroup untuk Projek
class ProjectModelAdmin(ModelAdmin):
  model = ProjectModel
  menu_label = 'Proyek Donasi'
  menu_icon = 'doc-full-inverse'
  #list yang di display di page admin wagtail

  list_display = ['title']
  
class ProjectDetailModelAdmin(ModelAdmin):
  model = ProjectDetailModel
  menu_label = 'Detail Proyek'
  menu_icon = 'doc-full-inverse'
  list_display = ['project_id','user_id']

#class StatusModelAdmin(ModelAdmin):
#  model = StatusModel
#  menu_label = 'Status Proyek Donasi'
#  menu_icon = 'doc-full-inverse'
#  list_display = ['status']
  
class RequestProjectModelAdmin(ModelAdmin):
  model = RequestProjectModel
  menu_label = 'Request Proyek'
  menu_icon = 'doc-full-inverse'
  list_display = ['subject']
  
class UserProfileModelAdmin(ModelAdmin):
  model = UserProfileModel
  menu_label = 'User Profile'
  menu_icon = 'doc-full-inverse'
  list_display = ['user']

class VolunteerStatusModelAdmin(ModelAdmin):
  model = VolunteerStatusModel
  menu_label = 'Volunteer Status'
  menu_icon = 'doc-full-inverse'
  list_display = ['project_id', 'user_id', 'status']

#Model untuk Event
#class EventModelAdmin(ModelAdmin):
#  model = EventModel
#  menu_label = 'Event'
#  menu_icon = 'doc-full-inverse'
#  list_display = ['nama_event']
#
#class DonationModelAdmin(ModelAdmin):
#  model = DonationModel
#  menu_label = 'List Donasi'
#  menu_icon = 'doc-full-inverse'
#  list_display = ['nama']
#
#class ResponseModelAdmin(ModelAdmin):
#  model = ResponseModel
#  menu_label = 'Response Kode'
#  menu_icon = 'doc-full-inverse'
#  list_display = ['kode_respon']

class QnAAdmin(ModelAdmin):
  model = QnAModel
  menu_label = 'Questions and Answers'
  menu_icon = 'help'
  list_display = ['konteks']
  
class SubscriberAdmin(ModelAdmin):
  model = SubscriberModel
  menu_label = 'Subscriber'
  menu_icon = 'mail'
  list_display = ['email']
  
class ProjectModelAdminGroup(ModelAdminGroup):
  menu_label = 'Donasi'
  menu_icon = 'folder-open-inverse'
  menu_order = 200
  items = (ProjectModelAdmin,ProjectDetailModelAdmin,UserProfileModelAdmin,VolunteerStatusModelAdmin,RequestProjectModelAdmin)

#
# class EventModelAdminGroup(ModelAdminGroup):
#   menu_label = 'Event'
#   menu_icon = 'folder-open-inverse'
#   menu_order = 200
#   items = (EventModelAdmin)

modeladmin_register(ProjectModelAdminGroup)
modeladmin_register(QnAAdmin)
modeladmin_register(SubscriberAdmin)