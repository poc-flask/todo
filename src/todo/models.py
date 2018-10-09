from datetime import datetime
from flask_sqlalchemy import BaseQuery

from core.models import (
    db,
    TimestampMixin
)

#################################################
# Todo model and query set
#################################################

class TodoQuery(BaseQuery):

    def completed(self):
        """
        Filter completed todos
        """
        return self.filter_by(completed=True)

    def uncompleted(self):
        """
        Filter uncompleted todos
        """
        return self.filter_by(completed=False)

    def by_owner_and_id(self, user_id, id):
        """
        Filter Todo by owner and todo id
        """
        return self.by_owner(user_id) \
            .by_id(id)

    def by_owner(self, user_id):
        """
        Filter Todo by owner
        """
        return self.filter_by(user_id=user_id)

    def by_id(self, id):
        """
        Filter Todo by Id
        """
        return self.filter_by(id=id)

class Todo(db.Model, TimestampMixin):
    query_class = TodoQuery

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)
    title = db.Column(db.Unicode(100))
    due_date = db.Column(db.DateTime())
    completed = db.Column(db.Boolean(), default=False)
    completed_date = db.Column(db.DateTime())

    @classmethod
    def create_todo(cls, data):
        todo = Todo(**data)
        db.session.add(todo)
        db.session.commit()
        return todo

    def update(self, data):
        for key,value in data.items():
            setattr(self, key, value)

        if self.completed:
            self.completed_date = datetime.utcnow()
        else:
            self.completed_date = None

        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
