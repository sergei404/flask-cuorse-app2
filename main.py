from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
from form import BookingForm, RequestForm, SortTeacherForm
from utils import getGoals, getTeachers, getFilterTeachers,\
    getTeacherGoals, weekdays, getTeacher, practice
import json

app: Flask = Flask(__name__)
csrf = CSRFProtect(app)
SECRET_KEY = 'zxscdfg8uygfeplmzsw2'
app.config["SECRET_KEY"] = SECRET_KEY

@app.route('/')
def render_main():
    return render_template('index.html', goals=getGoals(),
                           teachers=getTeachers())


@app.route('/all/', methods=["GET", "POST"])
def render_all():
    form = SortTeacherForm()
    teachers_sort = getTeachers()
    if request.method == "POST":
        select= form.select.data
        if select == 'rating':
            teachers_sort.sort(key=lambda x: x["rating"], reverse=True)
        elif select == 'price_up':
            teachers_sort.sort(key=lambda x: x["price"], reverse=True)
        elif select == 'price_down':
            teachers_sort.sort(key=lambda x: x["price"])
        return render_template('all.html', form=form, teachers=teachers_sort)

    return render_template('all.html', teachers=teachers_sort, form=form)


@app.route('/request/')
def render_request():
    form = RequestForm()
    return render_template('request.html', form=form)


@app.route('/goal/<goal>/')
def render_goal(goal):
    if not getGoals()[goal]:
        return render_not_found(
            f"{goal} - такой цели обучения нет.")
    return render_template('goal.html',
                           teachers=getFilterTeachers(getTeachers(), goal),
                           goal=getGoals()[goal])


@app.route('/profiles/<int:teacher_id>/')
def render_teacher_profile(teacher_id):
    teacher = getTeacher(getTeachers(), teacher_id)
    goals = getTeacherGoals(getGoals(), teacher['goals'])
    if not teacher:
        return render_not_found(f"К сожалению, такого преподавателя нет")

    return render_template('profile.html', teacher=teacher, goals=goals,
                           weekdays=weekdays)


@app.route('/request_done/', methods=["GET", "POST"])
def render_request_done():
    form = RequestForm()
    if request.method == "POST" and form.validate_on_submit():
        user_goal = form.goal.data
        practice_time = form.practice_time.data
        user_name = form.name.data
        user_phone = form.phone.data

        user_data = {
            "time": practice[practice_time],
            "goal": getGoals()[user_goal][0],
            "phone": user_phone,
            "name": user_name,
        }

        with open("db.json", "a", encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False)

        return render_template(
            "request_done.html", user=user_data)

    return render_not_found("Для начала подайте заявку на подбор.")


@app.route('/booking/<int:id>/<day>/<time>/')
def render_booking(id, day, time):
    form = BookingForm()
    day_ru = weekdays[day[:3]][0]
    teacher = getTeacher(getTeachers(), id)
    if not teacher:
        return render_not_found(
            f"К сожалению, такого преподавателя не существует."
        )

    form.class_day.data = day
    form.time.data = time
    form.tutor_id.data = id
    return render_template('booking.html',
                           teacher=teacher, day=day_ru,
                           time=time, form=form)


@app.route('/booking_done/', methods=["GET", "POST"])
def render_booking_done():
    form = BookingForm()
    if request.method == "POST" and form.validate_on_submit():
        client_name = form.name.data
        client_phone = form.phone.data
        class_day = form.class_day.data
        time = form.time.data
        tutor_id = form.tutor_id.data

        user_data = {
            "client_name": client_name,
            "client_phone": client_phone,
            "class_day": class_day,
            "time": time,
            "tutor_id": tutor_id,
        }
        with open("db.json", "a", encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False)

    return render_template('booking_done.html',
            day=weekdays[class_day[:3]][0],
            time=time,
            name=client_name,
            phone=client_phone,
            tutor=getTeacher(getTeachers(), tutor_id),
        )

@app.errorhandler(404)
def render_not_found(message="По вашему запросу ничего не найдено"):
    return render_template("error.html", message=message), 404


if __name__ == '__main__':
    app.run(debug=True)
