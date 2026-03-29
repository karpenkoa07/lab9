from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    term = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        term = request.form.get("term","").strip()

        if company and term.isdigit():
            db.session.add(Jobs(company=company, term=int(term)))
            db.session.commit()

        return redirect("/")

    jobs = Jobs.query.all()
    total_term = sum(job.term for job in jobs)
    return render_template("index.html", jobs=jobs, total_term=total_term)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    job = Jobs.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect("/")

@app.route("/clear", methods=["POST"])
def clear():
    db.session.query(Jobs).delete()
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

