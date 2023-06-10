from datetime import datetime
from tokenize import TokenError
from rest_framework import serializers
from .EmailerService import *
from .RandomGenerator import *
from .models import  City, Country, State, User, UserProfile
from xml.dom import ValidationErr
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken

class CountrySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Country
        fields =['id', 'country_name', 'country_code']  
        required = True

class StateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = State
        fields =['id', 'country', 'state_name', 'state_code']  
        required = True
    country = CountrySerializer    

class CitySerializer(serializers.ModelSerializer):    
    class Meta:
        model = City
        fields =['id', 'state', 'city_name']  
        required = True
    state = StateSerializer         

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =['id', 'profile_pic']  
        required = True

class UserSerializer(serializers.ModelSerializer):     
    id = serializers.IntegerField(read_only=True)
    user_code = serializers.CharField(max_length=20, default=RandomGenerator.user_code()) 
    email = serializers.EmailField(max_length=255) 
    city = serializers.PrimaryKeyRelatedField(many=True, queryset=Country.objects.all())
    country = serializers.PrimaryKeyRelatedField(many=True, queryset=State.objects.all())  
    state = serializers.PrimaryKeyRelatedField(many=True, queryset=City.objects.all())  
    password = serializers.CharField() 
    password2 = serializers.CharField()
    class Meta:
        model = User
        fields = '__all__'
        required =True
    country = CountrySerializer
    state = StateSerializer
    city = CitySerializer    

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        print(attrs)
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password does't match")
        return attrs
    
    def create(self, validated_data):
        print("validating : ", validated_data)        
        return User.objects.create_user(**validated_data)    

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['email', 'password']       
    

class UserPasswordChange(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True) 
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True) 
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        print(attrs)
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password does't match")
        user.set_password(password)
        user.save()
        return attrs

class UserPasswordForgotLink(serializers.Serializer):
    email = serializers.EmailField(max_length=255) 
    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     print(email)
    #     if User.objects.filter(email=email).exists:
    #         user = User.objects.get(email=email)
    #         uid= urlsafe_base64_encode(force_bytes(user.id))
    #         print("Encoded user is: ", uid)
    #         token =PasswordResetTokenGenerator().make_token(user )
    #         print("Generated token: ", token)
    #         link ="http://127.0.0.1:9000/password_reset/"+uid+'/'+token
    #         print("Generated link: ", link)
    #         body="Click following link to reset password"+link
    #         # data ={
    #         #     "subject": "Rest Password",
    #         #     "body":body,
    #         #     "to_email": email,
    #         # }
    #         # EmailerService.email_sender(data)
    #         return attrs
    #     else:
    #         raise ValidationErr("Your email address is not valid")

class UserPasswordForgot(serializers.Serializer):
    user =""
    token ="" 
    try:    
        password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True) 
        password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
        
        def validate(self, attrs):
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid= self.context.get('uid')
            token = self.context.get('token')
            print(attrs)
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password does't match")
            id =smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationErr("This link for password reset is invalid or expired")
            user.set_password(password)
            user.save()
            return attrs        
    except DjangoUnicodeDecodeError as e:
        PasswordResetTokenGenerator().check_token(user, token)
        raise  ValidationErr("This link for password reset is invalid or expired")

class UserProfileSerializer(serializers.ModelSerializer):   
    country = serializers.SerializerMethodField('get_country')  
    state = serializers.SerializerMethodField('get_state')  
    city = serializers.SerializerMethodField('get_city') 
    user_deatils = UserImageSerializer()
    def get_country(self, obj): 
        country = {}
        country_obj = Country.objects.filter(country_name=obj.country)
        if len(country_obj)>0:
            country = CountrySerializer(country_obj[0]).data
        else:
            country = country
        return country['country_name']
    
    def get_state(self, obj): 
        state = {}
        state_obj = State.objects.filter(state_name=obj.state)
        if len(state_obj)>0:
            state = StateSerializer(state_obj[0]).data
        else:
            state = state
        return state['state_name'] 
    
    def get_city(self, obj): 
        city = {}
        city_obj = City.objects.filter(city_name=obj.city)
        if len(city_obj)>0:
            city = CitySerializer(city_obj[0]).data
        else:
            city = city
        return city['city_name']    
    class Meta:
        model = User
        fields =['id', 'name', 'email', 'address', 'user_code', 'country', 'state', 'city', 'pin_code', 'mobile', 'user_deatils'] 
        required = True
    # country = CountrySerializer
    # state = StateSerializer
    # city = CitySerializer  


class LogoutSerializer(serializers.Serializer):
    refresh =serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as te:
            print(str(te))
            self.fail("Bad Token")

   