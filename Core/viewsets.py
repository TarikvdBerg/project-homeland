from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from Core.access_policies import (PasswordAccessPolicy,
                                  PasswordGroupAccessPolicy,
                                  SCTFUserAccessPolicy)
from Core.models import Password, PasswordGroup, SCTFUser
from Core.serializers import (PasswordGroupSerializer, PasswordSerializer,
                              SCTFUserSerializer)
from rest_framework.parsers import JSONParser
import io

class SCTFUserViewSet(viewsets.ModelViewSet):
    queryset = SCTFUser.objects.all()
    serializer_class = SCTFUserSerializer
    permission_classes = (SCTFUserAccessPolicy, )

    def list(self, request):
        user_set = self.queryset.filter(pk=request.user.id)
        serializer = SCTFUserSerializer(user_set, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        if str(request.user.id) != pk:
            return Response({"error": "Access to user denied"}, status=403)
        
        user = SCTFUser.objects.get(pk=pk)
        serializer = SCTFUserSerializer(user)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        if str(request.user.id) != pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request)

    def destroy(self, request, pk=None):
        if str(request.user.id) != pk:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.queryset.get(pk=pk).delete()

        return Response(status=200)

class PasswordGroupViewSet(viewsets.ModelViewSet):
    queryset = PasswordGroup.objects.all()
    serializer_class = PasswordGroupSerializer
    permission_classes = (PasswordGroupAccessPolicy, )

    def list(self, request):
        """
        list returns a JSON list of password groups that are associated
        with the currently logged in user.
        """
        passwordgroups = self.queryset.filter(user=request.user)
        serializer = PasswordGroupSerializer(passwordgroups, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        retrieve returns a single password group after checking
        if the group belongs to the logged in user
        """
        try:
            pwgroup = PasswordGroup.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.id != pwgroup.user.id:
            return Response({"error": "Access denied to password group"}, status=403)
            
        serializer = PasswordGroupSerializer(pwgroup)
        return Response(serializer.data)

    def create(self, request):
        stream = io.BytesIO(request.body)
        parsed_data = JSONParser().parse(stream)
        parsed_data['user_id'] = request.user.id

        serializer = PasswordGroupSerializer(data=parsed_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        try:
            pwgroup = PasswordGroup.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if pwgroup.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        stream = io.BytesIO(request.body)
        parsed_data = JSONParser().parse(stream)
        parsed_data['user_id'] = request.user.id

        serializer = PasswordGroupSerializer(instance=pwgroup, data=parsed_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        try:
            pwgroup = PasswordGroup.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if pwgroup.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        pwgroup.delete()
        return Response(status=status.HTTP_200_OK)


class PasswordViewSet(viewsets.ModelViewSet):
    queryset = Password.objects.all()
    serializer_class = PasswordSerializer
    permission_classes = (PasswordAccessPolicy, )

    def list(self, request):
        pw_groups_set = PasswordGroup.objects.filter(user=request.user)
        password_set = self.queryset.filter(parent_group__in=pw_groups_set)
        serializer = PasswordSerializer(password_set, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            password = self.queryset.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PasswordSerializer(password)
        return Response(serializer.data)
    
    def create(self, request):
        stream = io.BytesIO(request.body)
        parsed_data = JSONParser().parse(stream)

        try:
            pwgroup = PasswordGroup.objects.get(pk=parsed_data['parent_group'])
            if pwgroup.user != request.user:
                return Response({"error": "Access to password group denied"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"error": "Password Group not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PasswordSerializer(data=parsed_data)
        
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data)

    def update(self, request, pk=None):
        # TODO: Clean this nested try except
        try:
            password = Password.objects.get(pk=pk)
        except:
            return Response({"error": "Password not found"}, status=status.HTTP_404_NOT_FOUND)
        
        stream = io.BytesIO(request.body)
        parsed_data = JSONParser().parse(stream)

        try:
            pwgroup = PasswordGroup.objects.get(pk=parsed_data['parent_group'])
            if pwgroup.user != request.user:
                return Response({"error": "Access to password group denied"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PasswordSerializer(instance=password, data=parsed_data)
        
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        # TODO: Clean this nested try except
        try:
            password = Password.objects.get(pk=pk)
            try:
                if password.parent_group.user != request.user:
                    return Response({"error": "Access to password denied"}, status=status.HTTP_403_FORBIDDEN)
            except:
                return Response({"error": "Password Group not found"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"error": "Password not found"}, status=status.HTTP_404_NOT_FOUND)

        password.delete()
        return Response(status=status.HTTP_200_OK)
