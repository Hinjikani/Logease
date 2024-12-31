from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length
from faker import Faker
from Logease.models import Armada, User

faker = Faker("id_ID")

class ArmadaForm(FlaskForm):
    armada_name = StringField('Armada Name', validators=[DataRequired()])
    armada_phone = StringField('Armada Phone', validators=[DataRequired(), Length(min=10, max=15)])
    armada_email = StringField('Armada Email', validators=[DataRequired(), Length(min=2, max=120)])
    submit = SubmitField('Register Armada')
    
    def validate_armada_name(self, armada_name):
        armada = Armada.query.filter_by(armada_name=armada_name.data).first()
        if armada:
            raise ValidationError('That armada name is taken. Please choose a different one.')
    def validate_armada_phone(self, armada_phone):
        armada = Armada.query.filter_by(armada_phone=armada_phone.data).first()
        if armada:
            raise ValidationError('That phone number is taken. Please choose a different one.')
    def validate_armada_email(self, armada_email):
        armada = Armada.query.filter_by(armada_email=armada_email.data).first()
        if armada:
            raise ValidationError('That email is taken. Please choose a different one.')

class UserPrivilege(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    privilege = SelectField('Privilege', choices=[('admin', 'Admin'), ('user', 'User'), ('armada', 'Armada')], validators=[DataRequired()])
    submit = SubmitField('Change Privilege')

    def validate_user_id(self, user_id):
        user = User.query.filter_by(id=user_id.data).first()
        if not user:
            raise ValidationError('User not found.')