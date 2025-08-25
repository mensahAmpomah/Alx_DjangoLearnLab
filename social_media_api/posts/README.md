Posts & Comments API

 Endpoints
 `GET /posts/` — list (paginated), supports `?search=...` on `title`, `content`, `author__username`, and `?ordering=created_at|-created_at|title`
`POST /posts/` — create (auth)
`GET /posts/{id}/` — retrieve
`PUT|PATCH /posts/{id}/` — update (author only)
 `DELETE /posts/{id}/` — delete (author only)

 `GET /comments/` — list (paginated). Filter by `?post=<id>`
 `POST /comments/` — create (auth)
 `GET /comments/{id}/` — retrieve
 `PUT|PATCH /comments/{id}/` — update (author only)
 `DELETE /comments/{id}/` — delete (author only)

### Examples

Create Post
```http
POST /posts/
Authorization: Token <token>
Content-Type: application/json

{
  "title": "My first post",
  "content": "Hello, world!"
}