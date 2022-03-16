from api import app, db
from api.models.user import UserModel
import click


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:") or "admin"
    password = input("Password[default 'admin']:") or "admin"
    user = UserModel(username, password, role="admin", is_staff=True)
    if not user.id:
        print(f'User with username {username} already exists!')
    else:
        user.save()
        print(f"Superuser create successful! id={user.id}")


@app.cli.command('getallusers')
def get_all_users():
    """
    Get all users
    """
    users = UserModel.query.all()

    for num, user in enumerate(users, 1):
        print(f"{num}.User id: {user.id} {user.username}")


@app.cli.command('my-command')
@click.argument('param')
def my_command(param):
    """
    Demo command with param
    """
    print(f"Run my_command with param {param}")


@app.cli.command('remove-user')
@click.option("--all", default=False, is_flag=True)
@click.argument('username', default="")
def my_command(username, all):
    """
    Remove user by username
    """
    if all:
        UserModel.query.delete()
        db.session.commit()
        return
