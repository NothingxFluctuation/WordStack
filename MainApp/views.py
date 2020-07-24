from django.shortcuts import render
from MainApp.models import WordData, EnterpriseData, SubjectData
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from pdfminer.high_level import extract_text
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import csv
from django.utils.encoding import smart_str
import re
import os
import random
import string

# Create your views here.


@api_view(["POST"])
def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user_f = User.objects.filter(username=username)
            if user_f:
                user = User.objects.get(username=username)
                if user.is_active:
                    print("password", password)
                    boolean = user.check_password(password)
                    if boolean:
                        token, created = Token.objects.get_or_create(user=user)
                        return Response(
                            {
                                "OK": "You are signed in.",
                                "token_key": token.key,
                                "id": user.id,
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"Error": "Incorrect Credentials"},
                            status=status.HTTP_401_UNAUTHORIZED,
                        )
                else:
                    return Response(
                        {"Error": "User is not active."},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return Response(
                    {"Error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"Error": "Data not valid."}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {"Error": "Request Method Unavailable"}, status=status.HTTP_400_BAD_REQUEST
        )




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"OK", "Auth Token is deleted."}, status=status.HTTP_200_OK)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_word_data(request):
    word = request.POST.get("word",'')
    weight_kpi = request.POST.get("weight_kpi",'')
    variability_kpi = request.POST.get("variability_kpi",'')
    n_of_occurences = request.POST.get("n_of_occurences",'')
    n_of_spread = request.POST.get("n_of_spread",'')
    mux = request.POST.get("mux",'')
    Max = request.POST.get("max",'')

    if word:
        WordData.objects.create(word = word, 
            weight_kpi = weight_kpi,
            variability_kpi = variability_kpi,
            n_of_occurences = n_of_occurences,
            n_of_spread = n_of_spread,
            mux = mux,
            Max = Max,
            )
        return Response({"OK", "The data is saved to database."}, status=status.HTTP_200_OK)
    else:
        return Response({"Error", "No Good data provided."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_subject_data(request):
    first_name = request.POST.get('first_name','')
    middle_name = request.POST.get('middle_name','')
    last_name = request.POST.get('last_name','')
    if first_name or middle_name or last_name:
        SubjectData.objects.create(first_name = first_name,
            middle_name = middle_name,
            last_name = last_name,
            )
        return Response({"OK", "The data is saved to database."}, status=status.HTTP_200_OK)
    else:
        return Response({"Error", "No Good data provided."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_enterprise_data(request):
    enterprise_name = request.POST.get('enterprise_name','')
    enterprise_type = request.POST.get('enterprise_type','')
    country = request.POST.get('country','')
    city = request.POST.get('city','')
    if enterprise_name or enterprise_type or country or city:
        EnterpriseData.objects.create(enterprise_name = enterprise_name,
            enterprise_type = enterprise_type,
            country = country,
            city = city,
            )
        return Response({"OK", "The data is saved to database."}, status=status.HTTP_200_OK)
    else:
        return Response({"Error", "No Good data provided."}, status=status.HTTP_400_BAD_REQUEST)






def home(request):
    return render(request,'home.html')


@csrf_exempt
def handle_documents(request):
    if request.method == 'POST':
        try:
            documents = request.FILES.getlist('documents')
            doc_list = []
            for doc in documents:
                doc_name = default_storage.save(doc.name, doc)
                print(default_storage.path(doc_name))
                doc_list.append(default_storage.path(doc_name))
            if doc_list:
                references = []
                word = WordData.objects.all()
                subject = SubjectData.objects.all()
                enterprise = EnterpriseData.objects.all()
                for w in word:
                    if w.word in references:
                        pass
                    else:
                        references.append(w.word)
                for s in subject:
                    if s.first_name:
                        if s.first_name in references:
                            pass
                        else:
                            references.append(s.first_name)
                    if s.middle_name:
                        if s.middle_name in references:
                            pass
                        else:
                            references.append(s.middle_name)
                    if s.last_name:
                        if s.last_name in references:
                            pass
                        else:
                            references.append(s.last_name)
                for e in enterprise:
                    if e.enterprise_name:
                        if e.enterprise_name in references:
                            pass
                        else:
                            references.append(e.enterprise_name)
                    if e.country:
                        if e.country in references:
                            pass
                        else:
                            references.append(e.country)
                    if e.city:
                        if e.city in references:
                            pass
                        else:
                            references.append(e.city)
                print(references)

                doc_dic = {}
                for d in doc_list:
                    d_l = []
                    text = extract_text(d)
                    new_text = re.sub(r'[^\x00-\x7F]+','',text).strip()
                    for r in references:
                        if r.lower() in new_text.lower():
                            d_l.append(r)
                    d_new = d.split("\\")[-1]
                    doc_dic[d_new] = d_l
                print('doc_dic:',doc_dic)
                d_split = d.split('\\')[:-1]
                csv_p = '\\'.join(d_split)
                csv_fldr_rand = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
                csv_fldr = csv_p + "\\csv\\" + csv_fldr_rand
                if not os.path.exists(csv_fldr):
                    os.mkdir(csv_fldr)
                csv_f = csv_fldr + '\\matched_data.csv'
                infile = open(csv_f,'w')
                writer = csv.writer(infile)
                writer.writerow(list(doc_dic.keys()))
                dick = max(doc_dic, key=lambda k: len(doc_dic[k]))
                dick_len = len(doc_dic[dick])
                c = dick_len - 2
                count = 0
                while count < c:
                    rowl = []
                    for dock in doc_dic.keys():
                        len_list = len(doc_dic[dock])
                        if len_list <=count:
                            print('me hit..')
                            print('dock:',dock)
                            rowl.append(' ')
                        else:
                            print("rowdocK: ",doc_dic[dock][count])
                            rowl.append(doc_dic[dock][count])
                    count +=1
                    writer.writerow(rowl)
                for doc_dl in doc_list:
                    os.remove(doc_dl)
                infile.close()
                rsp = "http://127.0.0.1:8000/media/csv/" + csv_fldr_rand + "/matched_data.csv"
                return HttpResponse(rsp)
            else:
                return HttpResponse("no documents.")
        except:
            return HttpResponse("some error occurred.")
    else:
        return HttpResponse("method not allowed.")

