from app import db, create_app, cli
from app.blueprints.authentication.models import User

app = create_app()
cli.register(app)

@app.shell_context_processor
def shell_context():
    return {'db': db, 'User': User}