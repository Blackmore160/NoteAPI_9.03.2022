from api import Resource, abort, reqparse, auth, g
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(tags=['Users'])
class UserResource(MethodResource):
    @doc(description='Get user by ID')
    @doc(summary="Get User by ID")
    @marshal_with(UserSchema, code=200)
    @doc(responses={"404": {
           "description": "User not found"}
    })
    def get(self, user_id):
        # # language=YAML
        # """
        # Get User by id
        # ---
        # tags:
        #     - Users
        # parameters:
        #       - in: path
        #         name: user_id
        #         type: # integer
        #         required: true
        #         default: 1
        # responses:
        #     200:
        #         description: A single user item
        #         schema:
        #             id: User
        #             properties:
        #                 id:
        #                     type: # integer
        #                     description: user id
        #                     default: 1
        #                 username:
        #                     type: # string
        #                     description: The name of the user
        #                     default: Steven Wilson
        #                 is_staff:
        #                     type: # boolean
        #                     description: user is staff
        #                     default: false
        #
        # """

        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user, 200

    @doc(security=[{"basicAuth": []}])
    @doc(summary='Edit user')
    # @auth.login_required(role="admin")
    @auth.login_required
    @marshal_with(UserSchema, code=200)
    @use_kwargs({'username': fields.Str(required=True)})
    def put(self, user_id, **kwargs):
        # parser = reqparse.RequestParser()
        # parser.add_argument("username", required=True)
        # user_data = parser.parse_args()
        user = UserModel.query.get(user_id)
        user.username = kwargs["username"]
        user.save()
        return user, 200

    @doc(security=[{"basicAuth": []}])
    @doc(summary='User delete')
    @auth.login_required
    def delete(self, user_id):
        # author = g.user
        user_for_delete = UserModel.query.get(user_id)
        if not user_for_delete:
            abort(404, error=f"user {user_id} not found")

        user_for_delete.delete()
        return {}, 204
        # raise NotImplemented  # не реализовано!


@doc(tags=['Users'])
class UsersListResource(MethodResource):
    @doc(summary="Get all Users")
    @marshal_with(UserSchema(many=True), code=200)
    def get(self):
        # # language=YAML
        # """
        # Get all Users
        # ---
        # tags:
        #     - Users
        # """

        users = UserModel.query.all()
        return users, 200

    @doc(summary="Create new user")
    @marshal_with(UserSchema, code=201)
    @use_kwargs(UserRequestSchema, location=('json'))
    def post(self, **kwargs):
        # parser = reqparse.RequestParser()
        # parser.add_argument("username", required=True)
        # parser.add_argument("password", required=True)
        # user_data = parser.parse_args()
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user, 201
