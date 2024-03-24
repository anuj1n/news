from django.utils import timezone
import json
import secrets
import string
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import HttpResponse
from .models import Story
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index_view(request):
    return HttpResponse("Welcome to the API home page")

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        request.user = user
        if user is not None:
            login(request, user)
            response = HttpResponse("Login occurs", status=200)
            return response
        else:
           return HttpResponse({'error': 'Invalid username or password'})      
    else:
        return HttpResponse("method not allowed")
    
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        session_id = request.session.get('session_id')
        if 'user' in request.COOKIES:
            value = request.session['session_id']
        if request.user.is_authenticated:
            logout(request)
            del request.session['session_id']
            return HttpResponse("Logout successful", status=200, content_type='text/plain')
        else:
            return HttpResponse("No user logged in", status=400, content_type='text/plain')
    

def post_story(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))

            # Create and save the story
            headline=data.get('headline'),
            category=data.get('category'),
            region=data.get('region'),
            details=data.get('details')

            story = Story.objects.create(
                headline=headline,
                category=category,
                region=region,
                author=request.user,
                date=timezone.now(),  
                details=details
            )
            story.save()
            return HttpResponse('Story posted successfully', status=201)
        else:
           return HttpResponse("User not authenticated", status=401)
    else:
        return HttpResponse({'error': 'Method not allowed'}, status=405)
    
def get_stories(request):
    if request.method == 'GET':
        story_cat = request.GET.get('story_cat')
        story_region = request.GET.get('story_region')
        story_date = request.GET.get('story_date')

        stories = Story.objects.all()

        if story_cat:
            stories = stories.filter(category=story_cat)
        if story_region:
            stories = stories.filter(region=story_region)
        if story_date:
            stories = stories.filter(date=story_date)

        serialized_stories = [{
            'key': story.key,
            'headline': story.headline,
            'category': story.category,
            'region': story.region,
            'author': story.author.username, 
            'date': story.date,
            'details': story.details
        } for story in stories]

        return JsonResponse({'stories': serialized_stories}, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def delete_story(story_key):
    try:
        story = Story.objects.get(key=story_key)
        story.delete_story()
        return HttpResponse("Story deleted successfully")
    except Story.DoesNotExist:
        return HttpResponse("Story not found")
    except Exception as e:
        return HttpResponse(f"Failed to delete story. Error: {str(e)}")
    

def register_agency(request):
    if request.method == 'POST':
        data = request.POST  
        agency_name = data.get('agency_name')
        agency_url = data.get('url')
        agency_code = data.get('agency_code')

        return JsonResponse({'message': 'Registration successful'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)