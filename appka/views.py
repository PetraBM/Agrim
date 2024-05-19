from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import UserRegistrationForm
from .forms import UserEditForm
from .forms import ProfileEditForm
from .models import Profile, Commodity, CNCode, Country, Licence
import json

@login_required
def edit_user(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

    if request.method == "POST":
        user_form = UserEditForm(data=request.POST, instance= request.user)
        profile_form = ProfileEditForm(data= request.POST, instance=request.user.profile, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect("appka:dashboard")

    return render(request, "account/edit.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })



def register(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()

            Profile.objects.create(user= new_user)

            return render(request, "account/register_done.html", {"new_user": new_user})

    return render(request, "account/register.html", {"form": form})

def index(request):
    return render(request, "index.html")

def dashboard(request):
    return render(request, "dashboard.html")

def licence_create(request):
    return render(request, "licences/addnew.html")

def licence_search(request):
    return render(request, "licences/search.html")

def get_komodita(request):
    
    komodita=[]
    com = Commodity.objects.all()

    for c in com:
        komodita.append({"commodity_id":c.commodity_id,"name":c.commodity})

    return JsonResponse(komodita, safe=False)

def get_knkod(request):
        
        knkod=[]

        if request.method == "GET":
            id=request.GET.get('id')

            cncode = CNCode.objects.all().filter(commodity_id=id)

            for cn in cncode:
                knkod.append({"cn_id":cn.cncode_id,"KnKod":cn.cncode})
    
        return JsonResponse(knkod, safe=False)


def get_country(request):
    country = []
    cty = Country.objects.order_by('country')

    for c in cty:
        country.append({"country_id": c.country_id, "name": c.country})

    return JsonResponse(country, safe=False)


def get_knkod_detail(request):
    knkod={}
    if request.method == "GET":
        id=request.GET.get('id')
        with open('knkody.json', 'r', encoding="UTF8") as f:
            knkody = json.load(f)
        for kn in knkody:
            if kn["Id"]==int(id):
                knkod={"Id":kn["Id"],"KnKod":kn["KnKod"],"Name":kn["Name"],"KomoditaId":kn["KomoditaId"], "MnozstviJednotka":kn["MnozstviJednotka"]}

    return JsonResponse(knkod, safe=False)

def licence_save(request):
    retData={"Status":"error"}
    if request.method == "POST":
        idKomodita=request.POST.get('idKomodita')
        idKnKod=request.POST.get('idKnKod')
        idCountry = request.POST.get('idCountry')
        mnozstvi=request.POST.get('mnozstvi')
        licence=request.POST.get('licence')
        validity = request.POST.get('validity')
        quota_number=request.POST.get('quota')
        user = request.user
        idKnKod=int(idKnKod)
        ocncode=CNCode.objects.get(cncode_id=idKnKod)
        idCountry = int(idCountry)
        ocountry = Country.objects.get(country_id=idCountry)

        Licence.objects.create(licence_number=licence, licence_validity=validity, licence_quantity=mnozstvi, cncode=ocncode,
                              quota_number=quota_number, country=ocountry, username=user)

        retData={"Status":"ok"}

    return JsonResponse(retData, safe=False)

def licence_get(request):
    result=[]

    if request.method == "GET":
        id=request.GET.get('id')
        # print(id)


        licences = Licence.objects.filter(cncode__commodity__commodity_id=id)
        for lic in licences:
            # print(lic)
            result.append({'id':lic.licence_id,
                           'licence':lic.licence_number,
                           'cncode':lic.cncode.cncode,
                           'country': lic.country.country,
                           'quota': lic.quota_number,
                           'quantity': lic.licence_quantity,
                           'validity': lic.licence_validity
                           })

    return JsonResponse(result, safe=False)