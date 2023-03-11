from app import create_app, db
from app.models import *

app = create_app()

with app.app_context():
    try:
        input("CONFIRM?\n>> ")
        db.drop_all()
        db.create_all()
        db.session.commit()
    except Exception as _:
        print(_)
