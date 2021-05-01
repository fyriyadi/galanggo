from __future__ import unicode_literals

from django.db import models
#untuk dropdown di pilihan status donasi
from django import forms
import datetime
from datetime import date
from django.utils import timezone
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (
  FieldPanel, TabbedInterface, ObjectList
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.views.serve import generate_signature
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# randomize kode unik
from random import randint,random



#Buat link khusus image untuk di dump ke json
def generate_image_url(image, filter_spec):
    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))
    image_filename = image.file.name[len('original_images/'):]
    return url + image_filename

#untuk konten dropdown yang dipakai di status donasi
class StatusModel(models.Model):
  status = models.CharField("kategori status donasi", max_length=128, unique=True)

  panels = [
    FieldPanel('status'),
  ]

#query untuk loading data di StatusModel di status donasi
class CategoryIterable(object):
    def __iter__(self):
        db_cat = StatusModel.objects.all()
        cats = ()
        for i in db_cat:
          tup = (i.status, i.status)
          cats = (tup,) + cats
        return cats.__iter__()

cats_list = CategoryIterable()
kategori_status_donasi = forms.Select()
kategori_status_donasi.choices = cats_list


class ProjectModel(models.Model):
  title = models.CharField('judul project',max_length=200, default='')
  description = RichTextField('description',max_length=1024, default='')
  lokasi_project = models.CharField('lokasi project', max_length=200, default='')
  tanggal_awal_project = models.DateField('tanggal awal project', default=date.today)
  tanggal_akhir_project = models.DateField('tanggal akhir project', default=date.today)
  DONASI = 'donasi'
  VOLUNTEER = 'volunteer'
  DANDV = 'donasi_volunteer'
  REQ_CHOICES = (
    (DONASI, 'Donasi'),
    (VOLUNTEER, 'Volunteer'),
    (DANDV, 'Donasi dan Volunteer'),
  )
  requirement = models.CharField('kebutuhan', max_length=200, choices=REQ_CHOICES, default=DANDV)
  dana_terkumpul = models.IntegerField('dana terkumpul', default=0)
  dana_dibutuhkan = models.IntegerField('dana dibutuhkan', default=0)
  volunteer_terkumpul = models.IntegerField('volunteer terkumpul', default=0)
  volunteer_dibutuhkan = models.IntegerField('volunteer dibutuhkan', default=0)
  gallery_pic = models.ForeignKey('wagtailimages.Image', verbose_name='Gallery Pic', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
  gallery_pic_url = models.CharField( max_length=1024, blank=True)
  tag = models.CharField('tag', max_length=1024, default='')
  tanggal_awal_priority = models.DateField('tanggal awal priority', default=date.today)
  priority_status = models.BooleanField(default=False)
  
  
  panels = [
    FieldPanel('title'),
    FieldPanel('description'),
    FieldPanel('lokasi_project'),
    FieldPanel('tanggal_awal_project'),
    FieldPanel('tanggal_akhir_project'),
    FieldPanel('requirement'),
    FieldPanel('dana_dibutuhkan'),
    FieldPanel('volunteer_dibutuhkan'),
    ImageChooserPanel('gallery_pic'),
    FieldPanel('tag'),
    FieldPanel('tanggal_awal_priority'),
    FieldPanel('priority_status'),
  ]
  edit_handler = TabbedInterface([
    ObjectList(panels, heading='Project Panel')
  ])

  def __str__(self):
      return self.title

#Nantinya dipakai untuk perhitungan donasi
  # @property
  # def my_field(self):
  #     return self.title + self.description

  def as_dict(self):
    my_dict = {
      #define field baru
      #'something' : self.myfield,
      'title' : self.title,
      'description' : self.description,
      'lokasi_project' : self.lokasi_project,
      'tanggal_awal_project' : self.tanggal_awal_project,
      'tanggal_akhir_project' : self.tanggal_akhir_project,
      'requirement' : self.requirement,
      'dana_terkumpul' : self.dana_terkumpul,
      'dana_dibutuhkan' : self.dana_dibutuhkan,
      'volunteer_terkumpul' : self.volunteer_terkumpul,
      'volunteer_dibutuhkan' : self.volunteer_dibutuhkan,
      'tanggal_awal_priority' : self.tanggal_awal_priority,
      'priority_status' : self.priority_status,
      'gallery_pic_url' : self.gallery_pic_url,
      'tag' : self.tag,
      'id': self.id,
    }
    return my_dict

  def clean(self):
    super(ProjectModel, self).clean
    if not(self.gallery_pic is None):
      self.gallery_pic_url = '%s' % (generate_image_url(self.gallery_pic, 'original'))

class ProjectDetailModel(models.Model):
  project_id = models.ForeignKey(ProjectModel, related_name="project_id_detail")
  user_id = models.ForeignKey(User, related_name="project_detail_user")
  midtrans_code = models.CharField('kode midtrans', max_length=150, default="", blank=True)
  amount = models.IntegerField('jumlah donasi', default=0)
  status_donasi = models.CharField('status donasi', max_length=150, default="undefined")
  score = models.IntegerField('volunteer score', default=0)
  
  panels = [
    FieldPanel('project_id'),
    FieldPanel('user_id'),
    FieldPanel('midtrans_code'),
    FieldPanel('amount'),
    FieldPanel('status_donasi'),
    FieldPanel('score'),
  ]
  edit_handler = TabbedInterface([
    ObjectList(panels, heading='Detail Project Panel')
  ])
  
  def as_dict(self):
    my_dict = {
      'project_id' : self.project_id.id,
      'project_title' : self.project_id.title,
      'midtrans_code' : self.midtrans_code,
      'amount' : self.amount,
      'status_donasi' : self.status_donasi,
      'score' : self.score,
    }
    return my_dict

class VolunteerStatusModel(models.Model):
  project_id = models.ForeignKey(ProjectModel, related_name="project_volunteers")
  user_id = models.ForeignKey(User, related_name="user_volunteers")
  PENDING = 'pending'
  ACCEPT = 'accepted'
  REJECT = 'rejected'
  VOL_CHOICES = (
    (PENDING, 'Pending'),
    (ACCEPT, 'Accepted'),
    (REJECT, 'Rejected'),
  )
  status = models.CharField('status', max_length=200, choices=VOL_CHOICES, default=PENDING)
  
  panels = [
    FieldPanel('project_id'),
    FieldPanel('user_id'),
    FieldPanel('status'),
  ]
  edit_handler = TabbedInterface([
    ObjectList(panels, heading='Volunteer Status Panel')
  ])
  
  def as_dict(self):
    my_dict = {
      'project_id' : self.project_id,
      'user_id' : self.user_id,
      'status' : self.status,
    }
    return my_dict

class UserProfileModel(models.Model):
  user = models.OneToOneField(User, related_name="user_profile")
  phone = models.CharField('phone', max_length=200, default="", blank=True)
  address = models.CharField('address', max_length=200, default="", blank=True)
  city = models.CharField('city', max_length=200, default="", blank=True)
  postal_code = models.CharField('postal code', max_length=200, default="", blank=True)
  country_code = models.CharField('country code', max_length=200, default="", blank=True)
  occupation = models.CharField('occupation', max_length=200, default="", blank=True)
  about = RichTextField('deskripsi', max_length=1024, default="", blank=True)
  OWNER = 'owner'
  DONATUR = 'donatur'
  VOLUNTEER = 'volunteer'
  DANDV = 'donatur_volunteer'
  ROLE_CHOICES = (
    (OWNER, 'Project Owner'),
    (DONATUR, 'Donatur'),
    (VOLUNTEER, 'Volunteer'),
    (DANDV, 'Donatur dan Volunteer'),
  )
  role = models.CharField(max_length=200, choices=ROLE_CHOICES, default=DANDV)
  
  def as_complete_dict(self):
    user = self.user
    my_dict = {
      'username': user.username,
      'email': user.email,
      'firstname': user.first_name,
      'lastname': user.last_name,
      'id': user.id,
      'profile': {
        'phone' : self.phone,
        'address' : self.address,
        'city' : self.city,
        'postal_code' : self.postal_code,
        'country_code' : self.country_code,
        'occupation' : self.occupation,
        'about' : self.about,
        'role' : self.role,          
      }
    }
    return my_dict

  def as_dict(self):
    my_dict = {
      'phone' : self.phone,
      'address' : self.address,
      'city' : self.city,
      'postal_code' : self.postal_code,
      'country_code' : self.country_code,
      'occupation' : self.occupation,
      'about' : self.about,
      'role' : self.role,
    }
    return my_dict

User.profile = property(lambda u: UserProfileModel.objects.get_or_create(user=u)[0])

def __user_str(self):
    return self.username

User.__str__ = __user_str

#class UserProfileDetailModel(models.Model):
#  user = models.ForeignKey(User, related_name="user_profile_detail")
#  id_project = models.ForeignKey(ProjectModel, related_name="project_id_profile")
#  donate_amount = models.IntegerField('donate amount', default=0)
#  volunteer_score = models.IntegerField('volunteer score', default=0)

#  def as_dict(self):
#    my_dict = {
#      'user' : self.user,
#      'id_project' : self.id_project,
#      'donate_amount' : self.profile.donate_amount,
#      'volunteer_score' : self.profile.volunteer_score,
#    }
#    return my_dict

#@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
#6def save_profile(sender, instance, created, **kwargs):
#    user = instance
#    if created:
#        profile = UserProfileModel(user=user)
#        profile.save()

#class DonateModel (models.Model):
#  donatur = models.ForeignKey(User, related_name="user_donations")
#  project = models.ForeignKey(ProjectModel, related_name="project_id_donations")
#  nama_donatur = models.CharField('nama donatur', max_length=1024, default='anonim')
#  nilai_donasi = models.IntegerField('nilai donasi', default=0)
#  status_pembayaran = models.CharField('status pembayaran', max_length=1024, default='belum terverifikasi')
#  tanggal_donasi = models.DateField("tanggal donasi", default=date.today)

#  @classmethod
#  def create(cls, title):
#    book = cls(title=title)
    # do something with the book
#    return book
  #Nantinya dipakai untuk perhitungan donasi


  # @property
  # def nilai_transfer(self):
  #   kode_unik = randint(100,999)
  #   return self.nilai_donasi + kode_unik
#  @property
#  def nilai_transfer(self):
#   kode_unik = (self.id % 1000)
#   return self.nilai_donasi + kode_unik
#  @property
#  def kode_unik(self):
#   kode_unik = (self.id % 1000)
#   return kode_unik

#  def as_dict(self):
#    my_dict = {
#      'nilai_transfer': self.nilai_transfer,
#      'kode_unik': self.kode_unik,
#      'nama_donatur' : self.nama_donatur,
#      'nilai_donasi' : self.nilai_donasi,
#      'status_pembayaran' : self.status_pembayaran,
#      'tanggal_donasi' : self.tanggal_donasi,
#    }
#    return my_dict

#class DonationModel (models.Model):
#  id_project = models.ForeignKey(ProjectModel, related_name="project_id_donate")
#  nama = models.CharField('nama donatur', max_length=1024, default='anonim')
#  alamat = models.CharField("alamat donatur", max_length=1024, default='')
#  email = models.CharField("email donatur", max_length=1024, default='')
#  telephone = models.CharField("telephone donatur", max_length=200, default='')
#  nilai = models.IntegerField('nilai donasi', default=0)
#  status_pembayaran = models.CharField('status pembayaran', max_length=1024, default='belum terverifikasi')
#  tanggal_donasi = models.DateTimeField(auto_now_add=True, blank=True)
#  jenis_bank = models.CharField("jenis bank",max_length=1024, default='')
#  nomor_akun = models.CharField("nomor akun",max_length=1024, default='')


#  def as_dict(self):
#    my_dict = {
#      'id_project' : self.id_project,
#      'nama' : self.nama,
#      'alamat' : self.alamat,
#      'email' : self.email,
#      'telephone' : self.telephone,
#      'nilai' : self.nilai,
#      'tanggal_donasi' : self.tanggal_donasi,
#      'status_pembayaran' : self.status_pembayaran,
#      'jenis_bank' : self.jenis_bank,
#      'nomor_akun' : self.nomor_akun,
#    }
#    return my_dict

#class EventModel (models.Model):
#  nama_event = models.CharField('nama event', max_length=1024, default='')
#  deskripsi_event = RichTextField('deskripsi event',max_length=1024, default='')
#  lokasi_event = models.CharField('lokasi event',max_length=1024, default='')
#  tanggal_event = models.DateField("tanggal event", default=date.today)
#  waktu_event_mulai = models.TimeField("waktu mulai event", default=datetime.time(7, 00))
#  waktu_event_berakhir = models.TimeField("waktu akhir event", default=datetime.time(18, 00))
#  gambar_event = models.ForeignKey('wagtailimages.Image', verbose_name='Gallery Pic', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
#  gambar_event_url = models.CharField( max_length=1024, blank=True)
#  tag_event = models.CharField('tag event', max_length=1024, default='')

#  panels = [
#    FieldPanel('nama_event'),
#    FieldPanel('deskripsi_event'),
#    FieldPanel('lokasi_event'),
#    FieldPanel('tanggal_event'),
#    FieldPanel('waktu_event_mulai', widget=forms.TimeInput(format='%H:%M')),
#    FieldPanel('waktu_event_berakhir', widget=forms.TimeInput(format='%H:%M')),
#    ImageChooserPanel('gambar_event'),
#    FieldPanel('tag_event'),
#  ]
#  edit_handler = TabbedInterface([
#    ObjectList(panels, heading='Events')
#  ])

#  def as_dict(self):
#    my_dict = {
#      'nama_event' : self.nama_event,
#      'deskripsi_event' : self.deskripsi_event,
#      'lokasi_event' : self.lokasi_event,
#      'tanggal_event' : self.tanggal_event,
#      'waktu_event_mulai' : self.waktu_event_mulai,
#      'waktu_event_berakhir' : self.waktu_event_berakhir,
#      'gambar_event_url' : self.gambar_event_url,
#      'tag_event' : self.tag_event,
#    }
#    return my_dict

#  def clean(self):
#    super(EventModel, self).clean
#    if not(self.gambar_event is None):
#      self.gambar_event_url = '%s' % (generate_image_url(self.gambar_event, 'original'))

class QnAModel (models.Model):
  konteks = models.CharField('konteks QnA', max_length=1024, default='')
  pertanyaan = models.CharField('pertanyaan QnA', max_length=1024, default='')  
  jawaban = RichTextField('jawaban QnA',max_length=1024, default='')      

  panels = [
    FieldPanel('konteks'),
    FieldPanel('pertanyaan'),
    FieldPanel('jawaban'),    
  ]
  edit_handler = TabbedInterface([
    ObjectList(panels, heading='Questions and Answers')
  ])

  def as_dict(self):
    my_dict = {
      'konteks' : self.konteks,
      'pertanyaan' : self.pertanyaan,
      'jawaban' : self.jawaban,
    }
    return my_dict

class SubscriberModel (models.Model):
  email = models.CharField('alamat email subscriber', max_length=1024, default='')
  waktu_subscribe = models.DateField("waktu subscribe", default=date.today)          

  panels = [
    FieldPanel('email'),
    FieldPanel('waktu_subscribe'),    
  ]
  edit_handler = TabbedInterface([
    ObjectList(panels, heading='Subscriber')
  ])  
  
  def as_dict(self):
    my_dict = {
      'email' : self.email,
      'waktu_subscribe' : self.waktu_subscribe,      
    }
    return my_dict
    
#  def clean(self):
 #   super(EventModel, self).clean
  #  if not(self.gambar_event is None):
   #   self.gambar_event_url = '%s' % (generate_image_url(self.gambar_event, 'original'))

#class ResponseModel(models.Model):
#  kode_respon = models.CharField('kode respon', max_length=1024, default='')
#  status_respon = models.CharField('kode respon', max_length=1024, default='')
#  deskripsi_respon = RichTextField('deskripsi respon', max_length=1024, default='')

#  panels = [
#    FieldPanel('kode_respon'),
#    FieldPanel('status_respon'),
#    FieldPanel('deskripsi_respon'),
#  ]
#  edit_handler = TabbedInterface([
#    ObjectList(panels, heading='Status')
#  ])

#  def as_dict(self):
#    my_dict ={
#      'kode_respon':self.kode_respon,
#      'status_respon':self.status_respon,
#      'deskripsi_respon':self.deskripsi_respon,
#    }
#    return my_dict
    
class RequestProjectModel(models.Model):
  sender_name = models.CharField('nama pengirim',max_length=200, default='')
  sender_email = models.CharField('email pengirim',max_length=200, default='')
  phone = models.CharField('phone', max_length=200, default="")
  subject = models.CharField('subject',max_length=200, default='')
  description = RichTextField('description',max_length=1024, default='')
  lokasi_project = models.CharField('lokasi project', max_length=200, default='')
  DONASI = 'donasi'
  VOLUNTEER = 'volunteer'
  DANDV = 'donasi_volunteer'
  REQ_CHOICES = (
    (DONASI, 'Donasi'),
    (VOLUNTEER, 'Volunteer'),
    (DANDV, 'Donasi dan Volunteer'),
  )
  requirements = models.CharField('kebutuhan', max_length=200, choices=REQ_CHOICES, default=DANDV)
  send_datetime = models.DateField('tanggal pengiriman', default=date.today)
  
  panels = [
    FieldPanel('sender_name'),
    FieldPanel('sender_email'),
    FieldPanel('phone'),
    FieldPanel('subject'),
    FieldPanel('description'),
    FieldPanel('lokasi_project'),
    FieldPanel('requirements'),
    FieldPanel('send_datetime'),
  ]
  edit_handler = TabbedInterface([
    ObjectList(panels, heading='Request')
  ])

  def as_dict(self):
    my_dict ={
      'sender_name':self.sender_name,
      'sender_email':self.sender_email,
      'phone':self.phone,
      'subject':self.subject,
      'description':self.description,
      'lokasi_project':self.lokasi_project,
      'requirements':self.requirements,
      'send_datetime':self.send_datetime,
    }
    return my_dict