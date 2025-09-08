from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import ContactMessage, Department, Post
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone 
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout

def home(request):   
    # Récupérer les objets Department et Post depuis la base
    departments = Department.objects.all()
    posts = Post.objects.all()
    return render(request, 'index.html', {
        'departments': departments,
        'posts': posts
    })

# views.py
@require_POST
@csrf_exempt
def formulaire(request):
    try:
        # Récupération des données du formulaire
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department_value = request.POST.get('department')
        poste_value = request.POST.get('poste')
        status_value = request.POST.get('message')  # champ "status"
        
        # Récupération des informations de la requête
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referrer = request.META.get('HTTP_REFERER', '')

        # Validation simple des champs requis
        if not name or not email or not phone:
            return JsonResponse({
                'success': False, 
                'message': 'Les champs nom, email et téléphone sont obligatoires'
            })

        # Recherche des objets Department et Post
        department = None
        if department_value:
            department = Department.objects.filter(name__iexact=department_value).first()
        
        poste = None
        if poste_value:
            poste = Post.objects.filter(name__iexact=poste_value).first()

        # Création du message de contact
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            department=department,
            post=poste,
            status=status_value,
            ip=ip,
            user_agent=user_agent,
            referrer=referrer
        )

        # send mail to admin when a new message is created

        # mail = EmailMessage(
        #     subject='vous avez pris vous fonction bonjour de travail ' + name,
        #     body=' vous avez pris vous fonction bonjour de travail ' + name,
        #     from_email= settings.EMAIL_HOST_USER,
        #     to= [
        #         f'{email}'
        #     ],
        #     reply_to=[email]
        # )
        # mail.send()
         
        # message si en soumen apres 08h00 min
      
        # if datetime.now().hour == 8 and datetime.now().minute < 10 and status_value == "Present":
        #     ms = "vous avez pris vous fonction bonjour de travail"
        # else:
        #     ms = "Vous etes en retard vous vous reseverez  une penalite "
    

        return JsonResponse({
            'success': True, 
            'message': 'Formulaire soumis avec succès!'

        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': f'Une erreur est survenue: {str(e)}'
        })

@login_required
def confige(request):
    # compte le mobre de prensence et absence et le nombre de personne

    mbPresence = ContactMessage.objects.filter(status="Present").count()
    mbAbsence = ContactMessage.objects.filter(status="Fin de travail").count() 
    useradd = ContactMessage.objects.all()
    return render(request, 'dash/config.html',
    {
        'mbPresence': mbPresence,
        'mbAbsence': mbAbsence, 
        'useradds': useradd  
    })



def login_view(request):
    if request.user.is_authenticated:
        return redirect('configuration')  # Redirige si déjà connecté

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next') or 'configuration')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'login.html')




# login obligatoire pour exporter le csv administrateur
@login_required 
def exportcsv(request):
    # export csv 
    # Statistiques
    mbPresence = ContactMessage.objects.filter(status="Present").count()
    mbAbsence = ContactMessage.objects.filter(status="Fin de travail").count()
    total_users = ContactMessage.objects.count()
    en_retard = total_users - mbPresence - mbAbsence  # si tu veux calculer les "en retard"

    # Créer la réponse CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)

    # Ligne de titre
    writer.writerow([
        'Nom', 'Email', 'Phone', 'Department', 'Post', 'Status', 'Date', 'IP', 'Device'
    ])

    # Écrire toutes les données utilisateurs
    users = ContactMessage.objects.all()
    for user in users:
        writer.writerow([
            user.name, user.email, user.phone, 
            user.department.name if user.department else '',
            user.post.name if user.post else '',
            user.status, user.created_at, user.ip, user.user_agent
        ])

    # Ajouter une ligne vide pour séparer les stats
    writer.writerow([])

    # Ajouter les statistiques en bas
    writer.writerow([
        'Nombre de personnes présentes', mbPresence
    ])
    writer.writerow([
        'Nombre  qui en fini  de  travail', mbAbsence
    ])
   
    

    return response


@require_http_methods(["GET", "POST"])
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')