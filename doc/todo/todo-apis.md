## ToDo APIs

### POST /todos/
----------------------------
**Request**

```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
eyJuYmYiOjE1MzY2OTg3NjYsImlhdCI6MTUzNjY5ODc2NiwiZnJlc2giOmZhbHNlLCJqdGkiOiI1MGQwZTdkNy1jMTk5LTQ1NmMtOTE\
0ZC04MGIwYWVjMjNjNWEiLCJpZGVudGl0eSI6MSwiZXhwIjoxNTM2NzA1OTY2LCJ0eXBlIjoiYWNjZXNzIn0.\
Q9T8IcqoNpJyH63PTh1Et_JvwWkJ_S9vS-4-r4JHO6k" \
--request POST \
--data '{"title": "Task 01","due_date": "2018-09-10T16:21:07"}' \
http://127.0.0.1:5000/todos
```

**Response**

```
{
    "id": 1,
    "user_id": 1,
    "due_date": "2018-09-10T16:21:07",
    "title": "Task 01",
    "completed_date": null,
    "completed": false
}
```

### GET /todo/{id}
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
http://127.0.0.1:5000/todo/1
```

**Response**

```
{
    "id": 1,
    "user_id": 1,
    "due_date": "2018-09-10T16:21:07",
    "title": "Task 01",
    "completed_date": null,
    "completed": false}
```

### PUT /todo/{id}
----------------------------
**Request**

```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer \
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
eyJuYmYiOjE1MzY3NTg2NTIsImp0aSI6IjZmYTc2NDdhLWRmODQtNGQ1MS1iZGFlLTdjMjQxMDAxOGQ2NyIsInR5cGUiOiJhY2Nlc3MiLCJ\
pYXQiOjE1MzY3NTg2NTIsImZyZXNoIjpmYWxzZSwiZXhwIjoxNTM2NzY1ODUyLCJpZGVudGl0eSI6MX0.\
emmEqWbRIrQtB0if7Ry-2GrcDs_6vgHe9CWeTTqN1bA" \
--request PUT \
--data '{"title": "Task 01 update","due_date": "2018-09-11T16:21:07"}' \
http://127.0.0.1:5000/todo/1
```

**Response**

```
{
    "id": 1,
    "user_id": 1,
    "completed_date": null,
    "title": "Task 01 update",
    "due_date": "2018-09-11T16:21:07",
    "completed": null
}
```

### DELETE /todo/{id}
----------------------------
**Request**

```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer \
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
eyJuYmYiOjE1MzY3NTg2NTIsImp0aSI6IjZmYTc2NDdhLWRmODQtNGQ1MS1iZGFlLTdjMjQxMDAxOGQ2NyIsInR5cGUiOiJhY2Nlc3MiLCJ\
pYXQiOjE1MzY3NTg2NTIsImZyZXNoIjpmYWxzZSwiZXhwIjoxNTM2NzY1ODUyLCJpZGVudGl0eSI6MX0.\
emmEqWbRIrQtB0if7Ry-2GrcDs_6vgHe9CWeTTqN1bA" \
--request DELETE \
http://127.0.0.1:5000/todo/1
```

**Response**

```
{
    "message": "OK"
}
```

### GET /todos/completed
----------------------------
**Request**

```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
eyJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTM2Nzc0MzgzLCJqdGkiOiI4ZDQxODAzNC0wZmI2LTRjODQtYmU3Ni1jZDdmNzFkMTJkYzMiLCJpZ\
GVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJuYmYiOjE1MzY3NjcxODMsImlhdCI6MTUzNjc2NzE4M30.\
BVhtCxgh40UDR6cpsH7IGwOgiOYwrJ_T2vAbIfsOOpA" \
--request GET \
http://127.0.0.1:5000/todos/completed
```

**Response**

```
[{
    "id": 6,
    "completed": true,
    "user_id": 1,
    "title": "Task 06 - Update",
    "due_date": "2018-09-10T17:21:07",
    "completed_date": "2018-09-12T15:56:10"
}]
```

### GET /todos/uncompleted
----------------------------
**Request**

```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.\
eyJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTM2Nzc0MzgzLCJqdGkiOiI4ZDQxODAzNC0wZmI2LTRjODQtYmU3Ni1jZDdmNzFkMTJkYzMiLCJpZ\
GVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJuYmYiOjE1MzY3NjcxODMsImlhdCI6MTUzNjc2NzE4M30.\
BVhtCxgh40UDR6cpsH7IGwOgiOYwrJ_T2vAbIfsOOpA" \
--request GET \
http://127.0.0.1:5000/todos/uncompleted
```

**Response**

```
[
    {
        "id": 2,
        "completed": false,
        "user_id": 1,
        "title": "Task 01",
        "due_date": "2018-09-10T16:21:07",
        "completed_date": null
    }, {
        "id": 3,
        "completed": false,
        "user_id": 1,
        "title": "Task 01",
        "due_date": "2018-09-10T16:21:07",
        "completed_date": null
    }
]
```