'''проверка прав на работу со всем ресурсом  
 def has_permission(self, request, view):'''

from rest_framework.permissions import BasePermission

# не используется
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user == obj
    
# разрешение для таблицы Customuser
class IsOwner(BasePermission):
    ''' разрешает работу с записью только собственникам этого обьекта'''
    def has_object_permission(self, request, view, obj):
        return request.user == obj


# разрешение для таблицы Supplier
class IsOwnerSupplier(BasePermission):
    ''' разрешает работу с записью только собственникам этого обьекта'''
    def has_object_permission(self, request, view, obj):
        return request.user == obj.supplier
