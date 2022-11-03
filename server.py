import os
from flask import Flask, request, jsonify
from flask.views import MethodView
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from typing import Type
import pydantic

load_dotenv()
app = Flask("app")


class HttpError(Exception):
    def __init__(self, stats_code: int, message: str | dict | list):
        self.stats_code = stats_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({
        "status": "error",
        "message": error.message
    })
    response.status_code = error.stats_code
    return response


engine = create_engine(os.getenv("DSN"))
Base = declarative_base()
Session = sessionmaker(bind=engine)


class AdsModel(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), index=True, nullable=False)
    description = Column(String(300), nullable=False)
    creation_date = Column(DateTime, server_default=func.now())
    owner = Column(String(100), index=True, nullable=False)


Base.metadata.create_all(engine)


class CreateAdsSchema(pydantic.BaseModel):
    title: str
    description: str
    owner: str

    @pydantic.validator("title")
    def check_title(cls, value: str):
        if len(value) > 50:
            raise ValueError("Title must be less then 50 symbols.")
        return value

    @pydantic.validator("description")
    def check_description(cls, value: str):
        if len(value) > 300:
            raise ValueError("Description must be less then 300 symbols.")
        elif len(value) < 10:
            raise ValueError("So little description.")
        return value

    @pydantic.validator("owner")
    def check_owner(cls, value: str):
        if len(value) > 100:
            raise ValueError("Owner must be less then 100 symbols.")
        elif value == " ":
            raise ValueError("Wrong! Not owner.")
        return value


def validate(data_to_validate: dict, validation_class: Type[CreateAdsSchema]):
    try:
        validation_class(**data_to_validate).dict()
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


def get_by_id(item_id: int, orm_model: Type[AdsModel], session: Session):
    orm_item = session.query(orm_model).get(item_id)
    if orm_item is None:
        raise HttpError(404, "Ads not found.")
    return orm_item


class AdsView(MethodView):
    def get(self, ads_id: int):
        with Session() as session:
            ads = session.query(AdsModel).get(ads_id)
            if ads is None:
                raise HttpError(404, f"There are not ads with id: {ads_id}.")
            return jsonify({
                "ads title": ads.title,
                "ads description": ads.description,
                "owner": ads.owner
            })

    def post(self):
        json_data = request.json
        with Session() as session:
            new_ads = AdsModel(**validate(json_data, CreateAdsSchema))
            session.add(new_ads)
            session.commit()
            return jsonify({"status": "OK", "id": new_ads.id})

    def delete(self, ads_id: int):
        with Session() as session:
            ads = get_by_id(ads_id, AdsModel, session)
            if ads is None:
                raise HttpError(404, f"There are not ads with id: {ads_id}.")
            session.delete(ads)
            session.commit()
            return jsonify({"status": "successfully deleted"})


app.add_url_rule("/ads/<int:ads_id>", view_func=AdsView.as_view("ads_get"), methods=["GET", "DELETE"])
app.add_url_rule("/ads/", view_func=AdsView.as_view("ads_create"), methods=["POST"])

app.run()
