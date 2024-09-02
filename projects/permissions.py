from rest_framework.permissions import BasePermission

class IsInGroup(BasePermission):
    def __init__(self, group_name):
        self.group_name = group_name

    def has_permission(self, request, view):
        return request.user.groups.filter(name=self.group_name).exists()

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return IsInGroup('Manager').has_permission(request,view)
        return True

class IsDeveloperOrQA(BasePermission):
    def has_permission(self, request, view):
        return IsInGroup('Developer').has_permission(request,view) or IsInGroup('QA').has_permission(request,view)


class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Implement your logic to check if the user is allowed to modify the project
        return request.user in obj.members  # Example check