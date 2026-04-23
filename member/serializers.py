from rest_framework import serializers
from member.models import Member
from users.models import User

class MemberUserSerializer(serializers.ModelSerializer):
    """when we create member then we take information """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'address']
        read_only = ['id', 'email']
        
        
class MemberSerializer(serializers.ModelSerializer):
    """"""
    user = MemberUserSerializer(read_only=True)
    class Meta:
        model = Member
        fields = ['id', 'user', 'membership_date', 'created_at']
        read_only_fields = ['id', 'membership_date', 'created_at']
        

class CreateMemberSerializer(serializers.ModelSerializer):
    """Post / api/ members/ - authentication will convert into user to member"""
    class Meta:
        model = Member
        fields = ['id', 'membership_date']
        read_only_fields = ['id', 'membership_date']
        
    def validate(self, attrs):
        user = self.context['request'].user
        if Member.objects.filter(user=user).exists():
            raise serializers.ValidationError("You are already member of this library!")
        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Member.objects.create(user=user, **validated_data) #data unpacking
    
class UpdateMemberSerializer(serializers.ModelSerializer):
    """PUT/PATCH - update user personal info"""
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_number = serializers.CharField(source='user.phone_number', required=False, allow_blank=True)
    address = serializers.CharField(source='user.address', required=False, allow_blank=True)
    
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'phone_number', 'address']
        
    def update(self, instance, validated_data):
        #Nested user data alada kore seperated korbe
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        return super().update(instance, validated_data)
        