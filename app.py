from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField

# Flask application setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nmu_student_housing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Student model
class Student(db.Model):
    __tablename__ = 'students'
    id_student = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.Integer, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    secondname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

# Apartment model
class Apartment(db.Model):
    __tablename__ = 'apartment'
    id_apt = db.Column(db.Integer, primary_key=True)
    apt_num = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    fk_building = db.Column(db.Integer, db.ForeignKey('building.id_building'), nullable=False)
    lease_count = db.Column(db.Integer, default=0)


# Building model
class Building(db.Model):
    __tablename__ = 'building'
    id_building = db.Column(db.Integer, primary_key=True)
    building_num = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    total_floors = db.Column(db.Integer, nullable=False)

    apartments = db.relationship('Apartment', backref='building', lazy=True)

# Maintenance Request model
class MaintenanceRequest(db.Model):
    __tablename__ = 'maintenance_request'
    request_id = db.Column(db.Integer, primary_key=True)
    issue_description = db.Column(db.String(255), nullable=False)
    date_reported = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    fk_apartment = db.Column(db.Integer, db.ForeignKey('apartment.id_apt'), nullable=False)

    apartment = db.relationship('Apartment', backref='maintenance_requests')

# Lease model
class Lease(db.Model):
    __tablename__ = 'lease'
    lease_id = db.Column(db.Integer, primary_key=True)
    fk_student = db.Column(db.Integer, db.ForeignKey('students.id_student'), nullable=False)
    fk_apartment = db.Column(db.Integer, db.ForeignKey('apartment.id_apt'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    terms_and_conditions = db.Column(db.Text, nullable=True)

    student = db.relationship('Student', backref='leases')
    apartment = db.relationship('Apartment', backref='leases')

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Flask-Admin custom views
class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        if not current_user.is_admin:
            return redirect(url_for('home'))
        return super().index()
    def is_visible(self):
        # This view will not show up in the menu
        return False
    
# Create a new view class for the logout functionality
class LogoutMenuLink(MenuLink):
    def get_url(self):
        return url_for('logout')
    
class UserAdminView(ModelView):
    column_list = ['id', 'username', 'password', 'is_admin']
    form_columns = ['username', 'password', 'is_admin']
    form_extra_fields = {
        'password': SelectField(
            'Password',
            choices=[('admin123', 'admin123')]
        )
    }
    can_create = True
    can_edit = True
    can_delete = True

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        super(UserAdminView, self).on_model_change(form, model, is_created)

    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex

class StudentAdminView(ModelView):
    column_list = ['studentid', 'firstname', 'secondname', 'gender', 'phone', 'faculty', 'year']
    form_columns = ['studentid', 'firstname', 'secondname', 'gender', 'phone', 'faculty', 'year']
    can_create = True
    can_edit = True
    can_delete = True

    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex


class ApartmentAdminView(ModelView):
    column_list = ['apt_num', 'floor', 'building.building_num', 'lease_count']
    column_labels = {'building.building_num': 'Building Number', 'lease_count': 'Active leases'}
    form_columns = ['apt_num', 'floor', 'fk_building', 'lease_count']
    form_extra_fields = {
        'fk_building': QuerySelectField(
            'Building',
            query_factory=lambda: Building.query.all(),
            get_label='building_num'
        ),
        'lease_count': SelectField(
            'Active leases',
            choices=[('0', 'empty'), ('1', '1'), ('2', '2'), ('3', 'full')]
        )
    }
    can_create = True
    can_edit = True
    can_delete = True
    
    def on_model_change(self, form, model, is_created):
        model.fk_building = model.fk_building.id_building  # Extract the id from the Building object
        if is_created:
            building = Building.query.get(model.fk_building)
            if building and len(building.apartments) > building.capacity:
                raise ValueError("Building has reached its full capacity.")
        super(ApartmentAdminView, self).on_model_change(form, model, is_created)
    
    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex

class AdminLeaseView(ModelView):
    column_list = ['lease_id', 'student.firstname', 'student.secondname', 'apartment.apt_num', 'start_date', 'end_date', 'terms_and_conditions']
    column_labels = {
        'student.firstname': 'First Name',
        'student.secondname': 'Second Name',
        'apartment.apt_num': 'Apartment Number',
        'terms_and_conditions': 'Terms and Conditions'
    }
    form_columns = ['fk_student', 'fk_apartment', 'start_date', 'end_date', 'terms_and_conditions']
    form_extra_fields = {
        'fk_student': QuerySelectField(
            'Student',
            query_factory=lambda: Student.query.all(),
            get_label='firstname'
        ),
        'fk_apartment': QuerySelectField(
            'Apartment',
            query_factory=lambda: Apartment.query.all(),
            get_label='apt_num'
        )
    }
    can_create = True
    can_edit = True
    can_delete = True

    def on_model_change(self, form, model, is_created):
        model.fk_student = model.fk_student.id_student  # Extract the id from the Student object
        model.fk_apartment = model.fk_apartment.id_apt  # Extract the id from the Apartment object
        super(AdminLeaseView, self).on_model_change(form, model, is_created)
        
    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex

class AdminBuildingView(ModelView):
    column_list = ['building_num', 'location', 'capacity', 'total_floors']
    form_columns = ['building_num', 'location', 'capacity', 'total_floors']
    form_extra_fields = {
        'location': SelectField(
            'Location',
            choices=[('b1', 'Block 1'), ('b2', 'Block 2')]
        )
    }
    can_create = True
    can_edit = True
    can_delete = True
    
    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex
    
class MaintenanceRequestAdminView(ModelView):
    column_list = ['request_id', 'issue_description', 'date_reported', 'status', 'apartment.apt_num']
    column_labels = {
        'apartment.apt_num': 'Apartment Number'
    }
    form_columns = ['issue_description', 'status', 'fk_apartment']
    form_extra_fields = {
        'fk_apartment': QuerySelectField(
            'Apartment',
            query_factory=lambda: Apartment.query.all(),
            get_label='apt_num'
        ),
        'status': SelectField(
            'Status',
            choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')]
        )
    }
    can_create = True
    can_edit = True
    can_delete = True

    def on_model_change(self, form, model, is_created):
        model.fk_apartment = model.fk_apartment.id_apt  # Extract the id from the Apartment object
        super(MaintenanceRequestAdminView, self).on_model_change(form, model, is_created)
        
    def delete_model(self, model):
        try:
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex

# Initialize Flask-Admin
admin = Admin(app, name='NMU Panel', template_mode='bootstrap4', index_view=CustomAdminIndexView())
admin.add_view(StudentAdminView(Student, db.session))
admin.add_view(ApartmentAdminView(Apartment, db.session))
admin.add_view(AdminLeaseView(Lease, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(AdminBuildingView(Building, db.session))
admin.add_view(MaintenanceRequestAdminView(MaintenanceRequest, db.session))

# Add the logout link to the navbar
admin.add_link(LogoutMenuLink(name='Logout'))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        studentid = request.form['studentid']
        password = request.form['password']

        user = User.query.filter_by(id=studentid).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            # Redirect based on user role
            if user.is_admin:
                return redirect(url_for('admin.index'))
            return redirect(url_for('maintreq'))

        return 'Invalid credentials', 401

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    elif request.method == 'POST':
        studentid = request.form['studentid']
        firstname = request.form['firstname']
        secondname = request.form['secondname']
        gender = request.form['gender']
        password = request.form['password']
        conpassword = request.form['conpassword']
        phone = request.form['phone']
        faculty = request.form['faculty']
        year = request.form['year']

        if not studentid.isdigit():
            return "Student ID must be a number", 400

        if password != conpassword:
            return "Passwords do not match", 400

        if Student.query.filter_by(studentid=studentid).first():
            return "Student ID already exists", 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(
            id=studentid,
            username=f"{firstname} {secondname}",
            password=hashed_password
        )
        db.session.add(new_user)

        new_student = Student(
            id_student=studentid,  # Ensure the id matches the User id
            studentid=studentid,
            firstname=firstname,
            secondname=secondname,
            gender=gender,
            phone=phone,
            faculty=faculty,
            year=year
        )
        db.session.add(new_student)
        
        today = datetime.now()
        if today.month < 12 or (today.month == 12 and today.day <= 31):
            start_date = datetime(today.year, 10, 1)
            end_date = datetime(today.year + 1, 1, 20)
        else:
            start_date = datetime(today.year + 1, 2, 15)
            end_date = datetime(today.year + 1, 6, 15)

        # Select the first apartment that is not full based on gender
        if gender.lower() == 'male':
            apartment = Apartment.query.join(Building).filter(Building.location == 'b1', Apartment.lease_count < 3).first()
        else:
            apartment = Apartment.query.join(Building).filter(Building.location == 'b2', Apartment.lease_count < 3).first()
        
        if apartment:
            new_lease = Lease(
                fk_student=new_student.id_student,
                fk_apartment=apartment.id_apt,
                start_date=start_date,
                end_date=end_date,
                terms_and_conditions="accepted"
            )
            apartment.lease_count += 1
            db.session.add(new_lease)
            db.session.commit()  # Commit the changes to the apartment and lease
        else:
            return "No available apartments", 400

        return redirect(url_for('thankyou'))

@app.route('/maintreq', methods=['GET', 'POST'])
@login_required
def maintreq():
    if request.method == 'POST':
        issue_description = request.form['issue_description']

        # Get the current user's lease
        student = Student.query.filter_by(id_student=current_user.id).first()
        lease = Lease.query.filter_by(fk_student=student.id_student).first()
        if not lease:
            return "No lease found for the current user", 404

        # Create a new maintenance request
        new_request = MaintenanceRequest(
            issue_description=issue_description,
            fk_apartment=lease.fk_apartment
        )
        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for('requested'))

    # Get the current user's lease
    student = Student.query.filter_by(id_student=current_user.id).first()
    lease = Lease.query.filter_by(fk_student=student.id_student).first()
    if not lease:
        return "No lease found for the current user", 404

    apartment = Apartment.query.get(lease.fk_apartment)
    return render_template('maintreq.html', apartment=apartment)

@app.route('/thankyou')
@login_required
def thankyou():
    return render_template('thankyou.html')

@app.route('/policies')
def policies():
    return render_template('policies.html')

@app.route('/eligibility')
def eligibility():
    return render_template('eligibility.html')

@app.route('/requested')
@login_required
def requested():
    return render_template('requested.html')
    
# Initialize database
with app.app_context():
    db.create_all()
    ##ensure admin user exists
    if not User.query.filter_by(id=0).first():
        admin_user = User(
        id=0,
        username='admin',
        password=generate_password_hash('admin123', method='pbkdf2:sha256'),
        is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
    print("Admin user created with ID: 0 and password: admin123")

if __name__ == '__main__':
    app.run(debug=True)