import datetime
import json
from tokenize import TokenError
from requests import session
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from users.services import Link_Generator
from .models import City, Country, State, User, UserProfile
from .serializers import CitySerializer, CountrySerializer,  LogoutSerializer, StateSerializer, UserLoginSerializer, UserPasswordChange, UserPasswordForgot, UserPasswordForgotLink, UserProfileSerializer, UserSerializer
from django.contrib.auth import authenticate
# from users.renderer import customRenderer
from rest_framework_simplejwt.tokens import RefreshToken

#### JWT Authentication Functions Start #####
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    #session['token'] = str(refresh.access_token)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
#### JWT Authentication Functions Ends #####

###### Get Country, State, and City Function Start #####
@api_view(['GET'])
def country(request):    
    queryset = Country.objects.all()
    serializer = CountrySerializer(queryset, many=True)
    str_data=json.dumps(serializer.data)
    data =json.loads(str_data)
    #data = JSONRenderer().render(serializer.data) // Due to backslashes i dont want to use this method  
    return Response(data, status=200)

@api_view(['GET'])
def state(request, country_id):
    queryset = State.objects.filter(country = int(country_id))   
    serializer = StateSerializer(queryset, many=True)
    data=json.dumps(serializer.data)     
    return Response(data, status=200)

@api_view(['GET'])
def city(request, state_id):
    queryset = City.objects.filter(state = int(state_id))
    serializer = CitySerializer(queryset, many=True)    
    str_data=json.dumps(serializer.data)    
    print(str_data)  
    return Response(str_data, status=200)
###### Get Country, State, and City Function Start #####

################### User Functions Start #################
@api_view(['POST'])
def registeration(request):
    print("request hited.....", request.data)
    try: 
        # print(type(request.data))
        data = json.loads(request.data)    
        if data:       
            serializer = UserSerializer(data=data) 
            print(serializer)  
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                print(user)
                token =get_tokens_for_user(user)
                return Response({'token': token, "msg":"Registration Successfully"}, status=200)
            return Response({"msg":"Something went wrong, Please try later"}, status=200)
    except Exception as e:
        print(str(e))
        return Response(str(e), status=500)    
    return Response(str(serializer.errors), status=400)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_update(request, user_code=None):
    print("Request Hited.....")
    try:
        message="User details updated successfully"
        product = User.objects.filter(user_code=user_code).first()
        data = request.data  
        if data: 
            print("inside user update") 
            if product is None:
                message="User not found"
                return Response({"message":message}, status=404)
            if request.method == "PUT":   
                serializer = UserSerializer(instance=product, data=data)                 
                try:                    
                    if serializer.is_valid():
                        serializer.save()                        
                    return Response({"data":serializer.data, "message":message}, status=200)
                except Exception as e:
                    print(str(e)) 
                    return Response({"message":"Something went worng, please try later"}, status=500)                        
            elif request.method == "PATCH":
                serializer = UserSerializer(instance=product, data=data, partial=True)                               
                try:                    
                    if serializer.is_valid():
                        serializer.save()                        
                    return Response({"data":serializer.data, "message":message}, status=200)
                except Exception as e:
                    print(str(e)) 
                    return Response({"message":"Something went worng, please try later"}, status=500)                                      
        return Response({"message":"Nothing were found with request"}, status=400) 
    except Exception as e:
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500) 

@api_view(['POST'])
def login(request):
    try:
        message = "Login successfully"
        print(type(request.data))
        data = json.loads(request.data)  
        print(data)                  
        email = data['email']
        print(email)
        user = User.objects.filter(email=email)        
        if user is None:            
            message = "User does not exist"
            return Response({"message":message}, status=200)
        else:
            user_serializer = UserProfileSerializer(user, many=True)
            serializer = UserLoginSerializer(data=data)              
            if serializer.is_valid():                
                email = serializer.data.get('email')
                password = serializer.data.get('password')  
                print(email, password)      
                user = authenticate(request, email=email, password=password)                   
            if user is not None:
                token =get_tokens_for_user(user)
                print(token)
                login_time = datetime.datetime.now()                
                print(user_serializer.data)
                return Response({'token': token, "login_time":login_time, "user_info":user_serializer.data, "message":"Login Successfully"}, status=200)               
        return Response({"message":"Something went wrong, Please try again"}, status=500)     
    except Exception as e:
        print(str(e))
        return Response({"message":"Email or Password is not valid"}, status=400)    
   
@api_view(['POST'])
@permission_classes([IsAuthenticated])        
def password_change(request):
    data = json.loads(request.data)
    serializer = UserPasswordChange(data =data, context={'user':request.user})  
    if serializer.is_valid(raise_exception=True):       
        return Response({"message":"Your password changed successfully"}, status=200) 
    return Response(str(serializer.errors), status=400)

@api_view(['POST'])       
def forgot_password_link(request):
    data = json.loads(request.data) 
    # serializer = UserPasswordForgotLink(data=data)  
    # if serializer.is_valid(raise_exception=True):
    email = data['email']  
    if User.objects.filter(email=email).exists:
        user = User.objects.get(email=email) 
        link = Link_Generator(user)
        print(link)
        return Response({"msg":"Password Reset link generated", "link":link}, status=200) 
    # return Response(str(serializer.errors), status=400)

@api_view(['POST'])       
def forgot_password(request, uid, token,):
    serializer = UserPasswordForgot(data=request.data, context={"uid":uid, "token":token})  
    if serializer.is_valid(raise_exception=True):  
        return Response({"message":"Password Rest Successfully"}, status=200) 
    return Response(str(serializer.errors), status=400) 

@api_view(['POST'])  
@permission_classes([IsAuthenticated])      
def logout(request):
    try:
        serializer = LogoutSerializer(data=request.data)
        print(serializer) 
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Logout successfully"}, status=204)
        return Response({"msg": "Facing some issue"}, status=404)
    except TokenError as te:
        print(str(te))
################### User Functions Start #################


################### User Profile Functions Start #################
@api_view(['GET'])
@permission_classes([IsAuthenticated])        
def profile(request, user_code):
    try:        
        message = "User Details"
        user = User.objects.filter(user_code=user_code) 
        print(user)       
        if user is None:
            message = "No User were found"
            return Response({"message": message}, status=404)
        serializer = UserProfileSerializer(user, many=True)   
        print(serializer.data)  
        return Response({"message": message, "data":serializer.data}, status=200)
    except Exception as e:
        print(str(e))
        message = "Something went wrong, please try again"
        return Response({"message": message}, status=500)    

@api_view(['POST'])
@permission_classes([IsAuthenticated])        
def add_profile_pic(request):
    print(request.user)
    serializer = UserProfileSerializer(request.user)  
    print(serializer.data)   
    return Response(serializer.data, status=200) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])        
def update_profile_pic(request):
    print(request.user)
    serializer = UserProfileSerializer(request.user)  
    print(serializer.data)   
    return Response(serializer.data, status=200) 
@api_view(['GET', 'POST'])

@permission_classes([IsAuthenticated])        
def delete_profile_pic(request):
    print(request.user)
    serializer = UserProfileSerializer(request.user)  
    print(serializer.data)   
    return Response(serializer.data, status=200) 

################### User Profile Functions Start #################