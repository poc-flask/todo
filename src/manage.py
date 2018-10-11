import os

from core import app

# Load user, and todo module to the application
import auth
import user
import todo
import health

if __name__ == '__main__':
    app.run()
