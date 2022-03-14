from api.schemas.tag import TagSchema, TagRequestSchema
from api.models.tag import TagModel
from api import abort, auth
from api.schemas.note import NoteSchema
from api.resources.note import NoteModel
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        # print("note kwargs = ", kwargs)
        for tag_id in kwargs['tags']:
            tag = TagModel.query.get(tag_id)
            if not tag:
                abort(404, error=f'Tag with id={tag_id} not found')
            note.tags.append(tag)
        note.save()
        return note, 200


@doc(tags=['Tags'])
class TagResource(MethodResource):
    @marshal_with(TagSchema, code=200)
    @doc(summary="Get tag by id")
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"Tag with id={tag_id} not found")
        return tag, 200

    @doc(security=[{"basicAuth": []}])
    @doc(summary='Edit tag by id')
    @auth.login_required(role="admin")
    # @auth.login_required
    @marshal_with(TagSchema, code=200)
    @use_kwargs({'name': fields.Str(required=True)})
    def put(self, tag_id, **kwargs):
        # parser = reqparse.RequestParser()
        # parser.add_argument("username", required=True)
        # user_data = parser.parse_args()
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f'Tag with id={tag_id} not found')
        tag.name = kwargs["name"] or tag.name
        tag.save()
        return tag, 200

    @auth.login_required(role="admin")
    @doc(summary='Delete tag by id')
    @doc(responses={401: {"description": "Not authorization"}})
    @doc(responses={404: {"description": "Not found"}})
    @marshal_with(TagSchema, code=204)
    @doc(security=[{"basicAuth": []}])
    def delete(self, tag_id):
        # author = g.user
        tag_for_delete = TagModel.query.get(tag_id)
        if not tag_for_delete:
            abort(404, error=f"tag with id={tag_id} not found")

        tag_for_delete.delete()
        return tag_for_delete, 204


@doc(tags=['Tags'])
class TagListResource(MethodResource):
    @doc(summary="Get all tags")
    @marshal_with(TagSchema(many=True), code=200)
    def get(self):
        tags = TagModel.query.all()
        return tags, 200

    @doc(summary="Create new tag")
    @use_kwargs({"name": fields.Str(required=True)})
    # @use_kwargs(TagRequestSchema, location=("json"))
    @marshal_with(TagSchema, code=201)
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        if tag.id is None:
            abort(400, error=f'Tag with name={tag.name} already exist')
        return tag, 201