from rest_framework import permissions


def get_permissions_for_orders_and_item_in_order(action):
    if action in ['list', 'create']:
        permission_classes = [permissions.AllowAny]
    else:
        permission_classes = [permissions.IsAdminUser]
    return [permission() for permission in permission_classes]
