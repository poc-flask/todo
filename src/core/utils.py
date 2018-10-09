from datetime import datetime
from flask_restful import fields


def date_time_parsing(value, name):
    """
    Parse string to datetime
    """
    try:
        return datetime.strptime(value ,'%Y-%m-%dT%H:%M:%S')
    except Exception:
        raise ValueError("The parameter '{}' is should have this format %Y-%m-%dT%H:%M:%S. You gave us the value: {}".format(name, value))

class SerializeDateTime(fields.Raw):
    """
    Convert datetime to string for JSON Serialization.
    """

    def format(self, value):
        if type(value) is datetime:
            return value.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            return None
