from api import db
# from sqlalchemy.exc import IntegrityError
from api.models.class_additional import MixinModel

class TagModel(db.Model, MixinModel):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

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