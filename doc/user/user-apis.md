## ToDo APIs

### GET /user/{id}
----------------------------
**Request**

```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
eyJuYmYiOjE1MzY2OTg3NjYsImlhdCI6MTUzNjY5ODc2NiwiZnJlc2giOmZhbHNlLCJqdGkiOiI1MGQwZTdkNy1jMTk5LTQ1NmMtOTE\
0ZC04MGIwYWVjMjNjNWEiLCJpZGVudGl0eSI6MSwiZXhwIjoxNTM2NzA1OTY2LCJ0eXBlIjoiYWNjZXNzIn0.\
Q9T8IcqoNpJyH63PTh1Et_JvwWkJ_S9vS-4-r4JHO6k" \
--request GET \
http://127.0.0.1:5000/user/1
```

**Response**

```
{
    "id": 1,
    "first_name": "Tran",
    "access_token": null,
    "last_name": "Hoang"
}
```
