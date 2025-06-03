from rest_framework import permissions
from .models import Permission as UserPermission, Page

class HasPagePermission(permissions.BasePermission):
    """
    Checks if the authenticated user has the appropriate permission
    (view/create/edit/delete) for the Page specified in the request.
    Expecting 'page_id' in URL kwargs or request data.
    """

    def has_permission(self, request, view):
        # Superadmin: we assume superuser=True has full access to everything
        if request.user.is_superuser:
            return True

        # Determine action: map DRF view actions to our permission flags
        action = view.action  # e.g., 'list', 'retrieve', 'create', 'update', 'destroy'
        page_id = None

        # We expect the view to provide page_id either via URL kwarg or query param
        if 'page_id' in request.parser_context['kwargs']:
            page_id = request.parser_context['kwargs'].get('page_id')

        if not page_id and 'page_id' in request.data:
            page_id = request.data.get('page_id')

        if not page_id:
            return False  # cannot check permissions without knowing the page

        try:
            page = Page.objects.get(pk=page_id)
        except Page.DoesNotExist:
            return False

        try:
            perm = UserPermission.objects.get(user=request.user, page=page)
        except UserPermission.DoesNotExist:
            return False

        if action == 'list' or action == 'retrieve':
            return perm.can_view
        elif action == 'create':
            return perm.can_create
        elif action in ('update', 'partial_update'):
            return perm.can_edit
        elif action == 'destroy':
            return perm.can_delete

        return False
