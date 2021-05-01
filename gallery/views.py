from django.shortcuts import render
#ialngin kebutuhan cek csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
#untuk proteksi page.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
import json
from django.http import HttpResponse
from django.core import serializers

#start Library untuk validasi email
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
#end Library untuk validasi email

from datetime import date,datetime
from django.utils import timezone
from django.db.models import FloatField, Sum
from .midtrans import get_SNAP_token, MIDTRANS_API_CLIENT_KEY

#import logging
#logger = logging.getLogger(__name__)

#format date agar bisa di dump sebagai json
def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    # else:
    #     raise TypeError

from .token import token_login_required, generate_token


# Show all project data
# @login_required
def get_projects(request):
  projects = ProjectModel.objects.all()
  result = [project.as_dict() for project in projects]
  as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
  return HttpResponse (as_json, content_type="application/json")

def get_project(request, project_id):
  project = ProjectModel.objects.get(id=project_id)
  result = project.as_dict()
  as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
  return HttpResponse (as_json, content_type="application/json")

# Show all project data
# @login_required
#def get_events(request):
#  result = [event.as_dict() for event in events]
#  as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
#  return HttpResponse (as_json, content_type="application/json")

def get_qnas(request):
  qnas = QnAModel.objects.all()
  result = [qna.as_dict() for qna in qnas]
  as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
  return HttpResponse (as_json, content_type="application/json")

@token_login_required
def get_profile(request):
  user = request.user
  profile = request.user.profile
  user_dict = profile.as_complete_dict()
  as_json = json.dumps(user_dict, indent=2, ensure_ascii=False)
  #as_json = serializers.serialize('json', user_dict)
  return HttpResponse(as_json, content_type="application/json")
  
@token_login_required
def update_profile_view(request):
  user = request.user
  profile = request.user.profile
  if request.method == "GET":
    user_dict = profile.as_complete_dict()
    as_json = json.dumps(user_dict, indent=2, ensure_ascii=False)
    return HttpResponse(as_json, content_type="application/json")
  if request.method == "POST":
    body = request.body.decode("utf-8")
    postjson = json.loads(body.replace("'", '"'))
    save_firstname = postjson['firstname']
    save_lastname = postjson['lastname']
    save_phone = postjson['phone']
    save_address = postjson['address']
    save_city = postjson['city']
    save_postal_code = postjson['postal_code']
    save_country_code = postjson['country_code']
    try:
      user.first_name = save_firstname
      user.last_name = save_lastname
      user.save()
      profile.phone = save_phone
      profile.address = save_address
      profile.city = save_city
      profile.postal_code = save_postal_code
      profile.country_code = save_country_code
      profile.role = "donatur_volunteer"
      profile.save()
    except:
      return HttpResponse('Cannot update profile')
    else:
      temp_status = "Profile updated"
      return HttpResponse(temp_status)

#def temp_donation(request, projectid):
#  if request.method == "GET":
#    donations = DonationModel.objects.all()
#    result = [donation.as_dict() for donation in donations]
#    as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
#    return HttpResponse (as_json, content_type="application/json")
#  if request.method == "POST":
#    body = request.body.decode("utf-8")
#    postjson = json.loads(body.replace("'", '"'))
#    namadonatur = postjson['nama']
#    alamatdonatur = postjson['alamat']
#    emaildonatur = postjson['email']
#    telephone = postjson['telephone']
#    nilaidonasi = postjson['nilai']
#    nomorakun = postjson['nomor_akun']
#    jenisbank = postjson['jenis_bank']
#    namadonatur = request.POST['nama']
#    alamatdonatur = request.POST['alamat']
#    emaildonatur = request.POST['email']
#    handphonedonatur = request.POST['handphone']
#    nilaidonasi = request.POST['nilai']
#    tanggaldonasi = datetime.today()
#    statusdonasi = "Belum Terverifikasi"
#    try:
#      donasi = DonationModel.objects.create()
#      donasi.nama = namadonatur
#      donasi.alamat = alamatdonatur
#      donasi.email = emaildonatur
#      donasi.telephone = telephone
#      donasi.nilai= nilaidonasi
#      donasi.status_donasi = statusdonasi
#      donasi.tanggal_donasi = tanggaldonasi
#      donasi.id_project = projectid
#      donasi.nomor_akun = nomorakun
#      donasi.jenis_bank = jenisbank
#       donasi.nama_donatur = namadonatur
#       donasi.alamat_donatur = alamatdonatur
#       donasi.email_donatur = emaildonatur
#       donasi.handphone_donatur = handphonedonatur
#       donasi.nilai_donasi = nilaidonasi
#       donasi.status_donasi = statusdonasi
#       donasi.tanggal_donasi = tanggaldonasi
#      donasi.save()
#    except:
#      if donasi != None:
#        donasi.delete()
#      return HttpResponseRedirect('/donation/?error=registerfail')
#    else:
#      donations = DonationModel.objects.all()
#      result = [donation.as_dict() for donation in donations]
#      as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
#      return HttpResponse (as_json, content_type="application/json")
#      ok

#Check email      
def is_valid_email(email):
    try:
      validate_email(email)
      return True
    except ValidationError:
      return False       
            
def subscribe(request):
  #if request.method == "GET":
    #reject script???
  if request.method == "POST":
    body = request.body.decode("utf-8")
    postjson = json.loads(body.replace("'", '"'))
    emailsubscriber = postjson['email']      
    check = is_valid_email(emailsubscriber)
    try:
      if check == True:
        email_find = SubscriberModel.objects.filter(email=emailsubscriber)
        
        if email_find.count()>0:
          action_is = "Exists"
        else:
          subscribe = SubscriberModel.objects.create()
          subscribe.email = emailsubscriber         
          subscribe.save()
          action_is = "Success"
      else:
        action_is = "Not valid"        
        
    except:
      if subscribe != None:
        subscribe.delete()
      return HttpResponseRedirect('/subscribe/?error=subscribefail')
    else:          
      as_json= json.dumps({'action': action_is, 'email': emailsubscriber}, default=date_handler, indent=2, ensure_ascii=False)
      return HttpResponse (as_json, content_type="application/json")
      #ok
      
# @csrf_exempt
# @login_required
#def get_donation(request, projectid):
#  if request.method == "GET":
#    projects = ProjectModel.objects.all()
#    projects = ProjectModel.objects.filter(id=projectid)
#    CoWorkingModels.objects.filter(pk=coworking_id)
#    result = [project.as_dict() for project in projects]
#    as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
#    return HttpResponse (as_json, content_type="application/json")
#  if request.method == "GET":
#    return render(request,'donation.html', {
#       "projectid": projectid,
#    })
#  # untuk save data donasi
#  if request.method == "POST":
#    namadonatur = request.user.username#User.objects.get(username=request.user.username)
#    nilaidonasi = request.POST['nilaidonasi']
#    tanggaldonasi = datetime.today()
#    statusdonasi = 'Belum Terverifikasi'
#    try:
#      #dari parameter projectid yang direquest user
#      current_project=ProjectModel.objects.get(id=projectid)
#      #model dengan reference key ke User dan ke Project.
#      donasi = DonateModel.objects.create(donatur=request.user,project=current_project)
#      donasi.nama_donatur = namadonatur
#      donasi.nilai_donasi = nilaidonasi
#      donasi.status_donasi = statusdonasi
#      donasi.tanggal_donasi = tanggaldonasi
#      donasi.save()
#    except:
#      if donasi != None:
#        donasi.delete()
#      return HttpResponseRedirect('/donation/?error=registerfail')
#    else:
#    #   return HttpResponseRedirect('/confirm_donation/')
#      return HttpResponseRedirect('/profile')

# @login_required
#def confirm_donation(request,projectid):
#    if request.method == "GET":
#    #   current_user = User.objects.get(id = request.user.id)
#    #   current_user = User.objects.filter(id = request.user.id)
#    #   donates = current_user.donations.all()
#      donates = DonateModel.objects.all()
#      result = [donate.as_dict() for donate in donates]
#      as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
#      return HttpResponse (as_json, content_type="application/json")

#def donations_list(request):
#  if request.method == "GET":
#    donations = DonateModel.objects.all()
#    result = [donation.as_dict() for donation in donations]
#    as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
#    return HttpResponse (as_json, content_type="application/json")

@csrf_exempt
def register_view(request):
  if request.method == "GET":
    return render(request, 'register.html')
  if request.method == "POST":
    body = request.body.decode("utf-8")
    postjson = json.loads(body.replace("'", '"'))
    save_email = postjson['email']
    save_username = postjson['username']
    save_password = postjson['password']
    save_firstname = postjson['firstname']
    save_lastname = postjson['lastname']
    save_phone = postjson['phone']
    save_address = postjson['address']
    save_city = postjson['city']
    save_postal_code = postjson['postal_code']
    save_country_code = postjson['country_code']
    if save_email == '' or save_username == "" or save_password == '':
      return HttpResponse('Email, username and password cannot be empty')
    if User.objects.filter(email=save_email).exists():
      return HttpResponse('Duplicate email')
    try:
      user = User.objects.create_user(save_username,save_email,save_password)
      user.first_name = save_firstname
      user.last_name = save_lastname
      user.save()
      profile = user.profile
      profile.phone = save_phone
      profile.address = save_address
      profile.city = save_city
      profile.postal_code = save_postal_code
      profile.country_code = save_country_code
      profile.role = "donatur_volunteer"
      profile.save()
    except:
      return HttpResponse('Cannot create user')
    else:
      temp_status = "Register Success"
      return HttpResponse(temp_status)

#from django.middleware.csrf import get_token

def login_token_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return HttpResponse(generate_token(user.email))
        else:
            return JsonResponse({'result':"login failed"})

@csrf_exempt
def login_view (request):
  if request.method == "GET":
   # if request.GET['error'] == 'authfail':
    return render(request,'login.html')
  if request.method == "POST":
    #postjson = json.loads(request.body)
    #postjson = request.POST
    body = request.body.decode("utf-8")
    postjson = json.loads(body.replace("'", '"'))
    username = postjson['username']
    password = postjson['password']


    user = authenticate(username=username, password=password)

    if user is not None:
    # A backend authenticated the credentials, auth trus login usernya. object user dimasukin request
      login(request, user)
      #return HttpResponseRedirect('/profile/')

      temp_status = generate_token(user.email)
      return HttpResponse(temp_status)
    else:
    # No backend authenticated the credentials
      return HttpResponseRedirect('/login/?error=authfail')

# @token_login_required
def profile_view (request):
  #is_authenticated jadi opsi, tapi enak pake login_required.
  if request.user.is_authenticated:
    my_account = request.user
    return render(request, 'profile.html', context={
      'test' : my_account,
    })
  else:
    return HttpResponseRedirect('/login/')

@token_login_required
def pay_donate_view(request, project_id, amount):
    try:
      user = request.user
      c_project = ProjectModel.objects.get(id=project_id)
      c_donation = ProjectDetailModel(id=None,user_id=user,project_id=c_project,midtrans_code="",amount=amount,status_donasi="unpaid",score=0)
      c_donation.save()
      c_order_id = "GLG-{0}-{1}".format(str(c_project).zfill(8), str(c_donation.id).zfill(8))
      c_donation.midtrans_code = c_order_id
      c_donation.save()
      response = get_SNAP_token(request, user, c_order_id, amount)
      if response.status_code == 400:
          return HttpResponse('probably duplicate order_id ')
      else:
          token = response.json()['token']
          return render(request, 'snap.html', {'SNAP_TOKEN': token, 'CLIENT_KEY': MIDTRANS_API_CLIENT_KEY})
    except Exception as e:
      return HttpResponse('error while locating project with that project id')
  
    return HttpResponseRedirect('/login/')

@login_required
def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/login/')

#def get_responseCodeList(request):
#  responses = ResponseModel.objects.all()
#  result = [response.as_dict() for response in responses]
#  as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
#  return HttpResponse (as_json, content_type="application/json")

def get_priority(request):
  priority = ProjectModel.objects.filter(priority_status=True)
  result = [prior.as_dict() for prior in priority]
  as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
  return HttpResponse (as_json, content_type="application/json")
  
def get_statistics(request):
  donatur = ProjectDetailModel.objects.filter(amount__gt=0).values('user_id').annotate(total_amount=Sum('amount')).count()
  volunteer = ProjectDetailModel.objects.filter(score__gt=0).values('user_id').annotate(total_score=Sum('score')).count()
  project = ProjectModel.objects.all().count()
  donasi = ProjectDetailModel.objects.all().aggregate(total_amount=Sum('amount'))
  print(donasi)
  result = {
      'donatur_count': donatur, 
      'volunteer_count': volunteer, 
      'project_count': project, 
      'total_donation': donasi['total_amount']
  }
  as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
  return HttpResponse (as_json, content_type="application/json")
  
def request_project(request):
  if request.method == "GET":
    return render(request, 'request.html')
  if request.method == "POST":
    body = request.body.decode("utf-8")
    postjson = json.loads(body.replace("'", '"'))
    sender_name = postjson['sender_name']
    sender_email = postjson['sender_email']
    phone = postjson['phone']
    subject = postjson['subject']
    description = postjson['description']
    lokasi_project = postjson['lokasi_project']
    requirements = postjson['requirements']
    try:
      request = RequestProjectModel.objects.create()
      request.sender_name = sender_name
      request.sender_email = sender_email
      request.phone = phone
      request.subject = subject
      request.description = description
      request.lokasi_project = lokasi_project
      request.requirements = requirements
      request.send_datetime = datetime.today()
      request.save()
    except:
      return HttpResponse('Cannot request project')
    else:
      temp_status = "Request Success"
      return HttpResponse(temp_status)
      
def get_reqprojects(request, requirement):
  projects = ProjectModel.objects.filter(requirement=requirement)
  result = [project.as_dict() for project in projects]
  as_json= json.dumps(result, default=date_handler, indent=2, ensure_ascii=False)
  return HttpResponse (as_json, content_type="application/json")

@token_login_required
def register_volunteer(request, project_id):
    try:
      user = request.user
      project = ProjectModel.objects.get(id=project_id)
      if user.user_volunteers.filter(project_id=project).exists():
          return HttpResponse('Already registered as volunteer')
      else:
          project_volunteer = VolunteerStatusModel(id=None,user_id=user,project_id=project,status="pending")
          project_volunteer.save()
    except:
      return HttpResponse('error while locating project with that project id')
    return HttpResponse('Successfuly registered as volunteer')

def snap_finish_view(request):
    order_id = request.GET['order_id']
    amount = 0
    response = get_SNAP_token(order_id, amount)
    if response.status_code == 400:
        project_detail_id = int(order_id.split('-')[2])
        project_detail = ProjectDetailModel.objects.get(id=project_detail_id)
        project_detail.status = "paid"
        project_detail.save()
        return HttpResponse('finished snap request')
    else:
        return HttpResponse('failure with snap request')
        
@token_login_required
def get_volunteer_status(request):
  user = request.user
  status = user.user_volunteers.all()
  result = [stat.as_dict() for stat in status]
  as_json = json.dumps(result, indent=2, ensure_ascii=False)
  return HttpResponse(as_json, content_type="application/json")

@token_login_required
def get_volunteer_history(request):
  user = request.user
  projects = user.project_detail_user.filter(score__gt=0)
  result = [project.as_dict() for project in projects]
  as_json = json.dumps(result, indent=2, ensure_ascii=False)
  return HttpResponse(as_json, content_type="application/json")
  
@token_login_required
def get_donatur_history(request):
  user = request.user
  projects = user.project_detail_user.filter(amount__gt=0)
  result = [project.as_dict() for project in projects]
  as_json = json.dumps(result, indent=2, ensure_ascii=False)
  return HttpResponse(as_json, content_type="application/json")

@token_login_required
def get_history(request):
  user = request.user
  projects = user.project_detail_user.all()
  result = [project.as_dict() for project in projects]
  as_json = json.dumps(result, indent=2, ensure_ascii=False)
  return HttpResponse(as_json, content_type="application/json")