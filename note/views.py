from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Note
from .serializers import NoteSerializer

# Create your views here.

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    try:
        user = authenticate(
            username=request.data['username'],
            password=request.data['password']
        )
        if not user:
            return Response({'error', 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny,])
def register(request):
    try:
        user = User(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        return Response({'process':'user created'}, status=status.HTTP_201_CREATED)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET', 'POST'])
def note(request):
    try:
        user = request.user
        if request.method == 'GET':
            notes = user.notes.all()
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            note = Note(
                title=request.data['title'],
                content=request.data['content'],
                user=user
            )
            note.save()
            serializer = NoteSerializer(note)
            return Response(serializer.data)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def edit_note(request, id):
    try:
        user = request.user
        note = user.notes.get(id=id)
        if request.method == 'GET':
            pass
        elif request.method == 'PUT':
            if 'title' in request.data:
                note.title = request.data['title']
            elif 'content' in request.data:
                note.content = request.data['content']
            note.save()
        elif request.method == 'DELETE':
            note.delete()
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
