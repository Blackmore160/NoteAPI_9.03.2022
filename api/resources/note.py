from api import auth, abort, g, Resource, reqparse
from api.models.note import NoteModel
from api.schemas.note import note_schema, notes_schema, NoteSchema, NoteRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields
from api.models.tag import TagModel


@doc(tags=['Notes'])
class NoteResource(MethodResource):
    @auth.login_required
    @doc(summary="Get note by id", security=[{"basicAuth": []}])
    @doc(responses={404: {"description": "Not found"}})
    @marshal_with(NoteSchema, code=200)
    def get(self, note_id):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if author != note.author:
            abort(403)
        return note_schema.dump(note), 200

    @auth.login_required
    @doc(summary="Edit note by id", security=[{"basicAuth": []}])
    @doc(responses={404: {"description": "Not found"}})
    @doc(responses={403: {"description": "Forbidden"}})
    @use_kwargs(NoteRequestSchema, location='json')
    @marshal_with(NoteSchema, code=200)
    def put(self, note_id, **kwargs):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = g.user
        # parser = reqparse.RequestParser()
        # parser.add_argument("text", required=True)
        # parser.add_argument("private", type=bool)
        # note_data = parser.parse_args()
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        # note.text = note_data["text"]

        note.text = kwargs['text'] or note.text
        note.private = kwargs['private'] or note.private
        note.save()
        return note, 200

    @auth.login_required
    @doc(summary='Delete note by id', security=[{"basicAuth": []}])
    @doc(responses={401: {"description": "Not authorization"}})
    @doc(responses={404: {"description": "Not found"}})
    @marshal_with(NoteSchema, code=200)
    def delete(self, note_id):
        """
        Пользователь может удалять ТОЛЬКО свои заметки
        """
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if author != note.author:
            abort(403, error='Forbidden')
        note.delete()
        return note, 204


@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(summary="Get all Notes")
    @marshal_with(NoteSchema(many=True), code=200)
    def get(self):
        auth_user = g.user

        notes = NoteModel.query.all()
        return notes, 200

    @doc(security=[{"basicAuth": []}])
    @doc(summary='Create note')
    @marshal_with(NoteSchema, code=201)
    @use_kwargs(NoteRequestSchema, location='json')
    @auth.login_required
    def post(self, **kwargs):
        author = g.user
        # parser = reqparse.RequestParser()
        # parser.add_argument("text", required=True)
        # # Подсказка: чтобы разобраться с private="False",
        # #   смотрите тут: https://flask-restful.readthedocs.io/en/latest/reqparse.html#request-parsing
        # parser.add_argument("private", type=bool, required=True)
        # note_data = parser.parse_args()
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


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
