from .flaskapp import *
from flask import request, session, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from .database.models import User, File
from .database import add_delete


# session here: Flask does this is by using a signed cookie.





@app.route("/")
def index():
    # data = {"Data":"Some data here to be sent as dict (JSON)"}
    return render_template('index.html')

@app.route('/download/<int:file_id>')
def download_file(file_id):
    query = db.session.query(File).filter(File.file_id == file_id).first()
    fname = '_'.join(query.file_name.split())
    p = f"/Users/aknar/Desktop/python/assignment/website/saved files/{fname}"

    return send_file(p, as_attachment=True)


@app.route("/user/<int:user_id>")
def user(user_id, context=None):
    query = db.session.query(User).join(File).filter(File.user_id == user_id).first()

    if query:
        return render_template("user-page.html", context=query)
    else:
        query = db.session.query(User).filter(User.user_id == user_id).first()
        return render_template("user-page.html", context=query)


@app.route("/login", methods = ["GET", "POST"])
def login(context=None):
    if request.method == "POST":
        user = db.session.query(User).filter_by(login=request.form['email'], password=request.form['password']).first()
        if user:
            session['authenticated'] = True
            session['uid'] = user.user_id
            session['login'] = user.login
            session['fname'] = user.name
            session['sname'] = user.surname
            session['city'] = user.city
            session['profession'] = user.profession
            session['number'] = user.number

            return redirect(url_for("user", user_id=user.user_id))
        else:
            return render_template("login.html", context="The login or username were wrong")

    return render_template("login.html", context=context)


@app.route("/logout")
def logout():

    session.pop('authenticated', None)
    session.pop('uid', None)
    session.pop('login', None)
    return redirect(url_for('index'))


@app.route('/register', methods = ["GET", "POST"])
def register(context=None):
    if request.method == "POST":
        login = request.form['email']
        fname = request.form['name']
        sname = request.form['surname']
        pass1 = request.form['password']
        pass2 = request.form['password_conf']
        profession = request.form['profession']
        city = request.form['city']
        number = request.form['number']

        data = db.session.query(User).filter_by(login=request.form['email']).first()

        if data:
            return redirect(url_for("register", error="Already registered!"))
        elif pass1!=pass2:
            return redirect(url_for("register", error="Passowords do not match!"))
        else:
            add_delete.add_user(User(login=login,
                                name=fname,
                                surname=sname,
                                password=pass1,
                                profession=profession,
                                city=city,
                                number=number))

            return redirect(url_for("login", context="Succesfully registered!"))
    return render_template("register.html", context=context)



@app.route('/forgot', methods=["GET", "POST"])
def forgot():
    return render_template("forgot.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file(context=None):


    if request.method=="POST":
        f = request.files["file_to_save"]
        f.save(f"website/saved files/{secure_filename(f.filename)}")

        add_delete.add_file(File(
            file_name=f.filename,
            user_id=session['uid']
        ))
        return redirect(url_for('upload_file', context={"Status":"Successfully uploaded"}))
    return render_template("upload_file.html", context=context)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(port=5005, debug=True)


