from api import api, app, docs
from api.resources import note
from api.resources.user import UserResource, UsersListResource
from api.resources.auth import TokenResource
from api.resources.tag import TagResource, TagListResource
from config import Config

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(UsersListResource,
                 '/users')  # GET, POST
api.add_resource(UserResource,
                 '/users/<int:user_id>')  # GET, PUT, DELETE

api.add_resource(TokenResource,
                 '/auth/token')  # GET

api.add_resource(note.NotesListResource,
                 '/notes',  # GET, POST
                 )
api.add_resource(note.NoteResource,
                 '/notes/<int:note_id>',  # GET, PUT, DELETE
                 )
api.add_resource(TagListResource,
                 '/tags')  # GET, POST
api.add_resource(TagResource,
                 '/tags/<int:tag_id>')  # GET, PUT, DELETE
api.add_resource(note.NoteSetTagsResource,
                 '/notes/<int:note_id>/tags')  # PUT, DELETE
api.add_resource(note.NotesFilterResource,
                 '/notes/filter')
docs.register(UserResource)
docs.register(UsersListResource)
docs.register(note.NoteResource)
docs.register(note.NotesListResource)
docs.register(TokenResource)
docs.register(TagResource)
docs.register(TagListResource)
docs.register(note.NoteSetTagsResource)
docs.register(note.NotesFilterResource)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
