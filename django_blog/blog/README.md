Registration

User visits /register/.

register view uses CustomUserCreationForm (username + email + password).

On valid POST, the User is created; a Profile is automatically created by the post_save signal.

The view returns a success message and redirects to login.

Login

Django's LoginView handles authentication. On success it redirects to LOGIN_REDIRECT_URL (set to home).

Template blog/login.html presents the login form. CSRF tokens are used.

Logout

Django's LogoutView performs logout and renders a simple logout.html, then redirects to the homepage (or uses LOGOUT_REDIRECT_URL).

Profile Management

/profile/ is protected by @login_required so only authenticated users can access.

The view shows UserUpdateForm (username, email, first_name, last_name) and ProfileUpdateForm (bio, avatar).

When the user POSTs, the forms validate and data plus image (via request.FILES) are saved.

Security

CSRF protection: each form includes {% csrf_token %}.

Passwords are handled by Django's built-in hashing (PBKDF2/Argon2 if configured). You do not store plain text.

In production: use HTTPS, set DEBUG = False, configure ALLOWED_HOSTS, and store SECRET_KEY securely (env var).