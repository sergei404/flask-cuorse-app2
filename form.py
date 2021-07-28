import json
from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, StringField, HiddenField
from wtforms.validators import InputRequired
from utils import getGoals, practice

class SortTeacherForm(FlaskForm):
    select = SelectField("Сортировка преподавателей",
                         choices=[("random", "В случайном порядке"),
               ("rating", "Сначала лучшие по рейтингу"),
               ("price_up", "Сначала дорогие"),
               ("price_down", "Сначала недорогие")], default='random')

class RequestForm(FlaskForm):
    goal = RadioField(
        "Какая цель занятий?",
        choices=[
            (key, " ".join(value))
            for key, value in getGoals().items()
        ],
        default="travel",
    )

    practice_time = RadioField(
        "Сколько времени есть?",
        choices=[
            (key, value)
            for key, value in practice.items()
        ],
        default="l1",
    )

    name = StringField("Вас зовут", [InputRequired("Введите имя")])
    phone = StringField(
        "Ваш телефон", [InputRequired("Введите номер телефона")]
    )

class BookingForm(FlaskForm):
    tutor_id = HiddenField()
    class_day = HiddenField()
    time = HiddenField()
    name = StringField("Вас зовут", [InputRequired("Пожалуйста, введите ваше имя")])
    phone = StringField(
        "Ваш телефон", [InputRequired("Пожалуйста, введите ваш номер телефона")]
    )
