from Core.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

class SCTFUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # instance.username = validated_data.get('username')
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
    
    class Meta:
        model = SCTFUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'display_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PasswordGroupSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()

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
        fields = ['id', 'enc_name', 'user_id']
        read_only_fields = ('id', 'user_id')

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ['id', 'enc_name', 'enc_description', 'enc_password', 'parent_group']