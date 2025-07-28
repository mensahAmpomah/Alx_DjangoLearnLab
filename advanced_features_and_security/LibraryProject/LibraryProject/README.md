# Permissions & Group Setup

## Custom Permissions:
- can_view: Can view articles
- can_create: Can create articles
- can_edit: Can edit articles
- can_delete: Can delete articles

## Groups:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: All permissions

## Usage in Views:
- Views are protected using @permission_required('app_name.permission_code')