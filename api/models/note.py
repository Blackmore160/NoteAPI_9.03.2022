from api import db
from api.models.user import UserModel
from api.models.tag import TagModel
# from sqlalchemy.exc import IntegrityError
from api.models.class_additional import MixinModel

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('note_model_id', db.Integer, db.ForeignKey('note_model.id'), primary_key=True)
                )


class NoteModel(db.Model, MixinModel):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    text = db.Column(db.String(255), unique=False, nullable=False)
    private = db.Column(db.Boolean(), default=True, nullable=False)
    tags = db.relationship(TagModel, secondary=tags, lazy='subquery', backref=db.backref('notes', lazy=True))

    # def save(self):
    #     try:
    #         db.session.add(self)
    #         db.session.commit()
    #     except IntegrityError:  # Обработка ошибки "создание пользователя с НЕ уникальным именем"
    #         db.session.rollback()
    #
    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
