## Authentication APIs

### POST /auth/
----------------------------
**Request**

```
curl --header "Content-Type: application/json" \
--request POST \
--data '{"username": "tranhnb@gmail.com", "password": "123456"}' \
http://127.0.0.1:5000/auth
```

**Response**

```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1MzY2OTg3NjYsImlhdCI6MTUzNjY5ODc2NiwiZnJlc2giOmZhbHNlLCJqdGkiOiI1MGQwZTdkNy1jMTk5LTQ1NmMtOTE0ZC04MGIwYWVjMjNjNWEiLCJpZGVudGl0eSI6MSwiZXhwIjoxNTM2NzA1OTY2LCJ0eXBlIjoiYWNjZXNzIn0.Q9T8IcqoNpJyH63PTh1Et_JvwWkJ_S9vS-4-r4JHO6k"
}
```