from api import ma
from api.models.tag import TagModel


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TagModel
        fields = ('id', "name")
    _links = ma.Hyperlinks({
        'self': ma.URLFor('tagresource', values=dict(tag_id="<id>")),
        'collection': ma.URLFor('taglistresource')
    })


# Десериализация запроса(request)
class TagRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    name = ma.Str()
