from Core.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

def getCacheTimeout():
    return datetime.now() + timedelta(hours=6)

class SCTFUserSerializer(serializers.ModelSerializer):
    valid_until = serializers.ReadOnlyField(source='getCacheTimeout')

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False

        user.save()
        return user
    
    def update(self, instance, validated_data):
        # instance.username = validated_data.get('username')
        pw = validated_data.get('password', None)
        if pw != None and pw != "":
            instance.set_password(pw)

        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)


        instance.save()
        return instance
    
    class Meta:
        model = SCTFUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'display_name', 'valid_until']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PasswordGroupSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()
    valid_until = serializers.ReadOnlyField(source='getCacheTimeout')

    def create(self, validated_data):
        pwgroup = PasswordGroup.objects.create(
            enc_name = validated_data.get("enc_name"),
            user = SCTFUser.objects.get(pk=validated_data.get('user_id'))
        )
        pwgroup.save()

        return pwgroup
    
    def update(self, instance, validated_data):
        instance.enc_name = validated_data.get('enc_name', instance.enc_name)
        instance.save()
        return instance
    
    class Meta:
        model = PasswordGroup
        fields = ['id', 'enc_name', 'user_id', 'valid_until']
        read_only_fields = ('id', 'user_id')

class PasswordSerializer(serializers.ModelSerializer):
    valid_until = serializers.ReadOnlyField(source='getCacheTimeout')

    class Meta:
        model = Password
        fields = ['id', 'enc_name', 'enc_description', 'enc_username', 'enc_password', 'parent_group', 'valid_until']
