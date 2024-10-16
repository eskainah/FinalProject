from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    custom_id = serializers.CharField(source='user.custom_id', read_only=True)
                                      
    class Meta:
        model = Profile
        fields = ('first_name', 'middle_name', 'last_name', 'email', 'pic', 'school_name', 'custom_id')

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    custom_id = serializers.CharField(read_only=True)
    profile = ProfileSerializer(required=False, partial=True)  # Make profile optional and allow partial updates

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'middle_name', 'last_name', 'role', 'school_name', 'custom_id', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        role = attrs.get('role')
        school_name = attrs.get('school_name')

        # If the role is 'admin', ensure school_name is provided
        if role == User.ADMIN and not school_name:
            raise serializers.ValidationError({"school_name": "School name is required for admin users."})

        # If the role is 'teacher' or 'student', school_name should not be present
        if role in [User.TEACHER, User.STUDENT] and school_name:
            raise serializers.ValidationError({"school_name": "School name is only for admin users."})

        return attrs

    def create(self, validated_data):
        # Extract the user-specific fields
        first_name = validated_data.pop('first_name')
        middle_name = validated_data.pop('middle_name', '')
        last_name = validated_data.pop('last_name')
        school_name = validated_data.pop('school_name', None)  # Get school_name, default to None

        # Create the user object and set its fields
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],  # Pass the role
            first_name=first_name,  # Save the first name
            middle_name=middle_name,  # Save the middle name
            last_name=last_name,  # Save the last name
            school_name=school_name  # Save the school name
        )
        return user
    
    def update(self, instance, validated_data):
        # Update User fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if 'password' in validated_data:  # Update password if provided
            instance.set_password(validated_data['password'])
       
        instance.save()  # Save the User model

        profile = instance.profile    # Access the related Profile object

        # Update fields in the Profile model
        profile.first_name = validated_data.get('first_name', profile.first_name)
        profile.middle_name = validated_data.get('middle_name', profile.middle_name)
        profile.last_name = validated_data.get('last_name', profile.last_name)
        profile.pic = validated_data.get('pic', profile.pic)  # Update pic if provided
        profile.save() # Save the Profile model

        return instance

class SubAccountSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True) 
    custom_id = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'first_name', 'middle_name', 'last_name', 'custom_id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Ensure request context is available
        request = self.context.get('request')
        if request is None:
            raise serializers.ValidationError("Request context is required.")

        # Extract the user's role and other personal details
        first_name = validated_data.pop('first_name')
        middle_name = validated_data.pop('middle_name', '')
        last_name = validated_data.pop('last_name')
        school_admin = request.user

        # Ensure that only admins can create teachers and students
        if school_admin.role != User.ADMIN:
            raise serializers.ValidationError("Only admins can create sub-accounts.")

        # create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],  # Assign the role from the validated data
            school_admin=school_admin,  # Set the school admin reference
            first_name=first_name,  # Save the first name
            middle_name=middle_name,  # Save the middle name
            last_name=last_name,  # Save the last name
            school_name=school_admin.profile.school_name
        )

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
