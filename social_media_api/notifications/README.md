## Likes & Notifications

### Like a post
`POST /api/posts/posts/<pk>/like/`  (or adjust to your base path)
- Authentication required.
- Creates a Like and a Notification for the post author (if different).

### Unlike a post
`POST /api/posts/posts/<pk>/unlike/`
- Authentication required.
- Removes the Like record (does not delete previous notifications).

### Get notifications
`GET /api/notifications/` – returns your notifications (paginated).

### Mark notification as read
`POST /api/notifications/mark-read/<id>/` – mark one notification read.

### Mark all notifications read
`POST /api/notifications/mark-all-read/`
