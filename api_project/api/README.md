Authentication & Permission Setup:

- Token Authentication is used for API protection.
- Users must send a valid token in the Authorization header to access or modify posts.
- A token can be retrieved from /api/token/ using a valid username and password.
- Only the author of a post can edit or delete it. All users can view posts.

Permissions:
- List/Create: Any authenticated user
- Retrieve/Update/Delete: Only authenticated and authorized (author) users