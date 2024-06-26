import datetime

from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.mail import send_mail

from .forms import UserRegistrationForm
from .forms import UserEditForm
from .forms import ProfileEditForm
from .models import Profile, Commodity, CNCode, Country, Licence, ReqLicence
import json


@login_required
def edit_user(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

    if request.method == "POST":
        user_form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST, instance=request.user.profile, files=request.FILES)

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

            Profile.objects.create(user=new_user)

            return render(request, "account/register_done.html", {"new_user": new_user})

    return render(request, "account/register.html", {"form": form})


def index(request):
    return render(request, "index.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def licence_create(request):
    return render(request, "licences/addnew.html")


@login_required
def licence_search(request):
    return render(request, "licences/search.html")


@login_required
def licence_delete(request):
    retData = {"Status": "error"}

    if request.method == "POST":
        idLicence = request.POST.get('idLicence')
        lic = Licence.objects.get(licence_id=idLicence)
        lic.licence_active = 0
        lic.save()

        retData = {"Status": "ok"}

    return JsonResponse(retData, safe=False)


@login_required
def licence_list(request):
    result = []

    user = request.user

    licences = (Licence.objects
                .filter(user=user.profile)
                .filter(licence_validity__gte=datetime.datetime.now())
                .filter(licence_active=1))
    for lic in licences:
        result.append({'id': lic.licence_id,
                       'licence': lic.licence_number,
                       'cncode': lic.cncode.cncode,
                       'country': lic.country.country,
                       'quota': lic.quota_number,
                       'quantity': lic.licence_quantity,
                       'validity': lic.licence_validity
                       })

    context = {}
    context["list"] = result

    return render(request, "licences/my_licences.html", context=context)


@login_required
def request_list(request):
    req = ReqLicence.objects.all()

    result = []
    for r in req:
        print(r)
        result.append({'id': r.request_id,
                       'licence_id': r.licence.licence_id,
                       'licence': r.licence.licence_number,
                       'cncode': r.licence.cncode.cncode,
                       'country': r.licence.country.country,
                       'quota': r.licence.quota_number,
                       'quantity': r.licence.licence_quantity,
                       'reqquantity': r.request_quantity,
                       'holder': r.licence.user.username,
                       'requser': r.user.username
                       })

    context = {}
    context["list"] = result

    return render(request, "licences/list.html", context=context)


@login_required
def get_komodita(request):
    komodita = []
    com = Commodity.objects.all()

    for c in com:
        komodita.append({"commodity_id": c.commodity_id, "name": c.commodity})

    return JsonResponse(komodita, safe=False)


@login_required
def get_knkod(request):
    knkod = []

    if request.method == "GET":
        id = request.GET.get('id')

        cncode = CNCode.objects.all().filter(commodity_id=id)

        for cn in cncode:
            knkod.append({"cn_id": cn.cncode_id, "KnKod": cn.cncode})

    return JsonResponse(knkod, safe=False)


@login_required
def get_country(request):
    country = []
    cty = Country.objects.order_by('country')

    for c in cty:
        country.append({"country_id": c.country_id, "name": c.country})

    return JsonResponse(country, safe=False)


@login_required
def get_knkod_detail(request):
    knkod = {}
    if request.method == "GET":
        id = request.GET.get('id')
        with open('knkody.json', 'r', encoding="UTF8") as f:
            knkody = json.load(f)
        for kn in knkody:
            if kn["Id"] == int(id):
                knkod = {"Id": kn["Id"], "KnKod": kn["KnKod"], "Name": kn["Name"], "KomoditaId": kn["KomoditaId"],
                         "MnozstviJednotka": kn["MnozstviJednotka"]}

    return JsonResponse(knkod, safe=False)


@login_required
def licence_save(request):
    retData = {"Status": "error"}
    if request.method == "POST":
        # idKomodita = request.POST.get('idKomodita')
        idKnKod = request.POST.get('idKnKod')
        idCountry = request.POST.get('idCountry')
        quantity = request.POST.get('quantity')
        licence = request.POST.get('licence')
        validity = request.POST.get('validity')
        quota_number = request.POST.get('quota')

        ocncode = CNCode.objects.get(cncode_id=int(idKnKod))
        ocountry = Country.objects.get(country_id=int(idCountry))
        quantity= int(quantity)

        if quantity < 0:
            retData = {"Status": "The quantity must be higher than 0."}
        else:
            Licence.objects.create(licence_number=licence,
                                   licence_validity=validity,
                                   licence_quantity=quantity,
                                   cncode=ocncode,
                                   quota_number=quota_number,
                                   country=ocountry,
                                   user=request.user.profile)

            retData = {"Status": "ok"}

    return JsonResponse(retData, safe=False)


@login_required
def licence_get(request):
    result = []

    if request.method == "GET":
        id = request.GET.get('id')
        # print(id)

        licences = (Licence.objects
                    .filter(cncode__commodity__commodity_id=id)
                    .filter(licence_validity__gte=datetime.datetime.now())
                    .filter(licence_active=1))
        for lic in licences:
            # print(lic)
            result.append({'id': lic.licence_id,
                           'licence': lic.licence_number,
                           'cncode': lic.cncode.cncode,
                           'country': lic.country.country,
                           'quota': lic.quota_number,
                           'quantity': lic.licence_quantity,
                           'validity': lic.licence_validity
                           })

    return JsonResponse(result, safe=False)


@login_required
def request_save(request):
    retData = {"Status": "error"}
    if request.method == "POST":
        licence_id = request.POST.get('idLicence')
        licence_id = int(licence_id)

        request_quantity = request.POST.get('requested')
        request_quantity = int(request_quantity)

        lic = Licence.objects.get(licence_id=licence_id)

        if request_quantity > lic.licence_quantity:
            retData = {"Status": "The requested quantity exceeds the available quantity."}
        elif request_quantity < 0:
            retData = {"Status": "The requested quantity must be higher than 0."}
        else:
            ReqLicence.objects.create(licence=lic, request_quantity=request_quantity,
                                      request_date=datetime.datetime.now(), user=request.user.profile)

            context = {
                "to_username": lic.user.user.username,
                "licence_number": lic.licence_number,
                "quantity": request_quantity,
                "from_username": request.user.username,
                "from_email": request.user.email,
            }
            convert_to_html_content = render_to_string(
                template_name="email/licence_email.html",
                context=context
            )
            plain_message = strip_tags(convert_to_html_content)

            subject = 'Request of AGRIM transfer'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [lic.user.user.email]
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=email_from,
                recipient_list=recipient_list,
                html_message=convert_to_html_content,
            )

            retData = {"Status": "ok"}

    return JsonResponse(retData, safe=False)

# licence.user ->  licenceRequest
# holder - user

# subject = 'Request of AGRIM transfer'
# message = (f'Hello {holder - licence.user}, '
#            f'request for transfer of AGRIM licence {licence_id} for {request_quantity} kg has been sent by {request.user}.'
#            f'Best regards,'
#            f'AGRIM Transfers')
# email_from = settings.EMAIL_HOST_USER
# recipient_list = [licence.username, ]
# send_mail(subject, message, email_from, recipient_list)
