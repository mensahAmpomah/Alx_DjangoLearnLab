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


Blog Post CRUD Features
-----------------------

Routes:
- /posts/                : list all posts (ListView)
- /posts/new/            : create new post (CreateView) - login required
- /posts/<pk>/           : view post detail (DetailView)
- /posts/<pk>/edit/      : edit post (UpdateView) - author only
- /posts/<pk>/delete/    : delete post (DeleteView) - author only

Forms:
- PostForm (ModelForm) with fields: title, content. Author assigned automatically from request.user.

Permissions:
- Create: must be authenticated.
- Update/Delete: only the author can perform these actions (UserPassesTestMixin checks).

Templates:
- posts_list.html: displays paginated list with snippets (truncatechars).
- post_detail.html: full post display with edit/delete buttons for author.
- post_form.html: used for create/edit forms.
- post_confirm_delete.html: delete confirmation page.

Testing:
- Run server and manually test each route.
- Confirm unauthorized users cannot access new/edit/delete pages.

Notes:
- Add get_absolute_url to Post model to ensure proper redirect after create/update.
- Run migrations after changes: `python manage.py makemigrations && python manage.py migrate`.




Comment System — README

Routes:
- POST create (inline from post detail or separate page):
  /post/<post_pk>/comments/new/   (CommentCreateView) - login required

- Edit comment:
  /post/<post_pk>/comments/<pk>/edit/  (CommentUpdateView) - author only

- Delete comment:
  /post/<post_pk>/comments/<pk>/delete/ (CommentDeleteView) - author only

How to use:
- Anonymous users can read comments but must log in to comment.
- Logged-in users can post comments using the form on the post detail page.
- A comment author can edit or delete their own comments.
- Comments are linked to a post; deleting a post will delete its comments.

Developer notes:
- Model: Comment(post FK, author FK, content, created_at, updated_at).
- Form: CommentForm validates non-empty content.
- Views: Generic CBVs with LoginRequiredMixin and UserPassesTestMixin.
- Templates: comment_form.html, comment_confirm_delete.html, integrated list & form in post_detail.html
- Always include CSRF token for forms. Run migrations after adding the model.