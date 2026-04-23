from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from member.models import Member
from member import serializers as sz


class MemberViewSet(ModelViewSet):
    
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    def get_queryset(self):
        user = self.request.user
        #jodi se librarian or admin hoy tahole se sob dekhte parbe
        if user.is_staff:
            return Member.objects.select_related('user').all()
        #oi member shudu nijer data dekhte parbe 
        return Member.objects.select_related('user').filter(user=user)
    
    def get_serializer_class(self):
        if self.action == "create":
            return sz.CreateMemberSerializer
        if self.action in ['update', 'partial_update']:
            return sz.UpdateMemberSerializer
        return sz.MemberSerializer
    
    def get_permissions(self):
        #je kono authenticated user nijeke member banate parbe but na hole parbe nah
        if self.action == 'create':
            return [IsAuthenticated()]
        #shudu matro librarian or admin ei  sob member or user er list dekhte parbe
        if self.action == 'list':
            return [IsAdminUser()]
        
        # Retrieve, update, delete - eisob korte hole  authentication thakte hobe
        #kintu nijer ta chara onno karo ta access korte parbe na get_object e check hobe
        return [IsAuthenticated()]
    
    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        
        #librarian jeknono member ke access korte parbe
        if user.is_staff:
            return obj
        
        #member shudu nijer data access korte parbe
        if obj.user != user:
            raise PermissionDenied("You do not have permission to access to this member")
        return obj
    
    def destroy(self, request, *args, **kwargs):
        """shudu librarian delete korar access pabe"""
        if not request.user.is_staff:
            raise PermissionDenied("Only Librarian can delete members.")
        return super().destroy(request, *args, **kwargs)
    