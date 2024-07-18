from framework.auth.models import User
from framework.response import Response
from framework.app import app


@app.get('/users')
def list_users(request):
    users = User.manager.all()
    return Response(body=users)


@app.get('/users/{user_id}')
def with_params(request, user_id):
    user = User.manager.get(id=user_id)
    return Response(body=user)

