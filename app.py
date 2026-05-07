from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'careers-website-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///careers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    salary_range = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Job {self.title}>'


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30))
    cover_letter = db.Column(db.Text)
    linkedin_url = db.Column(db.String(300))
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))

    def __repr__(self):
        return f'<Application {self.first_name} {self.last_name}>'


def seed_jobs():
    if Job.query.count() == 0:
        sample_jobs = [
            Job(
                title="Senior Software Engineer",
                department="Engineering",
                location="Remote",
                job_type="Full-time",
                salary_range="$120,000 - $160,000",
                description="We are looking for a Senior Software Engineer to join our growing engineering team. You will work on building scalable backend services, contribute to architectural decisions, and mentor junior engineers. This role offers an exciting opportunity to shape the technical direction of our product.",
                requirements="5+ years of software engineering experience\nStrong proficiency in Python or Go\nExperience with cloud platforms (AWS, GCP, or Azure)\nFamiliarity with microservices and distributed systems\nExcellent communication and collaboration skills"
            ),
            Job(
                title="Product Designer",
                department="Design",
                location="San Francisco, CA",
                job_type="Full-time",
                salary_range="$95,000 - $130,000",
                description="Join our design team and help shape the visual identity and user experience of our products. You will collaborate closely with product managers and engineers to create intuitive, beautiful interfaces that delight our users.",
                requirements="3+ years of product design experience\nProficiency in Figma or Sketch\nStrong portfolio demonstrating UX/UI work\nExperience with user research and usability testing\nAbility to translate complex requirements into elegant designs"
            ),
            Job(
                title="Data Analyst",
                department="Data & Analytics",
                location="New York, NY",
                job_type="Full-time",
                salary_range="$80,000 - $110,000",
                description="We are seeking a Data Analyst to help us unlock insights from our data. You will work with cross-functional teams to define metrics, build dashboards, and drive data-informed decisions across the business.",
                requirements="2+ years of data analysis experience\nProficiency in SQL and Python or R\nExperience with BI tools (Tableau, Looker, or Power BI)\nStrong analytical and problem-solving skills\nExcellent presentation and storytelling ability"
            ),
            Job(
                title="Marketing Manager",
                department="Marketing",
                location="Remote",
                job_type="Full-time",
                salary_range="$90,000 - $120,000",
                description="Lead our marketing efforts and help us grow our brand presence. You will develop and execute marketing campaigns, manage content strategy, and drive user acquisition through a variety of channels.",
                requirements="4+ years of marketing experience\nProven track record of driving growth\nExperience with digital marketing channels (SEO, SEM, social media)\nStrong analytical skills and data-driven mindset\nExcellent written and verbal communication skills"
            ),
            Job(
                title="Customer Success Manager",
                department="Customer Success",
                location="Austin, TX",
                job_type="Full-time",
                salary_range="$70,000 - $95,000",
                description="Help our customers get maximum value from our product. You will onboard new clients, build strong relationships, and work proactively to ensure customer satisfaction and retention.",
                requirements="2+ years of customer success or account management experience\nExperience in SaaS environment preferred\nStrong interpersonal and communication skills\nAbility to manage multiple accounts simultaneously\nProblem-solving mindset with attention to detail"
            ),
            Job(
                title="DevOps Engineer",
                department="Engineering",
                location="Remote",
                job_type="Full-time",
                salary_range="$110,000 - $150,000",
                description="Join our infrastructure team to build and maintain the systems that power our platform. You will automate deployments, improve reliability, and ensure our services scale to meet growing demand.",
                requirements="4+ years of DevOps or infrastructure engineering experience\nStrong knowledge of Kubernetes and Docker\nExperience with CI/CD pipelines\nProficiency in infrastructure as code (Terraform, Ansible)\nExperience with monitoring and observability tools"
            ),
        ]
        for job in sample_jobs:
            db.session.add(job)
        db.session.commit()


@app.route('/')
def index():
    featured_jobs = Job.query.filter_by(is_active=True).order_by(Job.posted_date.desc()).limit(3).all()
    total_jobs = Job.query.filter_by(is_active=True).count()
    departments = db.session.query(Job.department).distinct().count()
    return render_template('index.html', featured_jobs=featured_jobs, total_jobs=total_jobs, departments=departments)


@app.route('/jobs')
def jobs():
    search = request.args.get('search', '')
    department = request.args.get('department', '')
    location_filter = request.args.get('location', '')
    job_type = request.args.get('job_type', '')

    query = Job.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            db.or_(
                Job.title.ilike(f'%{search}%'),
                Job.description.ilike(f'%{search}%'),
                Job.department.ilike(f'%{search}%')
            )
        )
    if department:
        query = query.filter(Job.department == department)
    if location_filter:
        query = query.filter(Job.location.ilike(f'%{location_filter}%'))
    if job_type:
        query = query.filter(Job.job_type == job_type)

    all_jobs = query.order_by(Job.posted_date.desc()).all()
    departments = db.session.query(Job.department).distinct().all()
    departments = [d[0] for d in departments]
    job_types = db.session.query(Job.job_type).distinct().all()
    job_types = [j[0] for j in job_types]

    return render_template('jobs.html', jobs=all_jobs, departments=departments,
                           job_types=job_types, search=search, selected_department=department,
                           selected_location=location_filter, selected_job_type=job_type)


@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    related_jobs = Job.query.filter_by(department=job.department, is_active=True).filter(Job.id != job_id).limit(3).all()
    return render_template('job_detail.html', job=job, related_jobs=related_jobs)


@app.route('/jobs/<int:job_id>/apply', methods=['GET', 'POST'])
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        cover_letter = request.form.get('cover_letter', '').strip()
        linkedin_url = request.form.get('linkedin_url', '').strip()

        if not first_name or not last_name or not email:
            flash('Please fill in all required fields.', 'error')
            return render_template('apply.html', job=job)

        application = Application(
            job_id=job_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            cover_letter=cover_letter,
            linkedin_url=linkedin_url
        )
        db.session.add(application)
        db.session.commit()
        flash(f'Your application for {job.title} has been submitted successfully!', 'success')
        return redirect(url_for('application_success', job_id=job_id))

    return render_template('apply.html', job=job)


@app.route('/jobs/<int:job_id>/apply/success')
def application_success(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('application_success.html', job=job)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_jobs()
    app.run(host='0.0.0.0', port=5000, debug=True)
