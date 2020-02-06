from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError, EqualTo, InputRequired
from app.models import User, Event
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField(validators = [DataRequired()])
    password = PasswordField(validators = [DataRequired()])
    submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):
    username = StringField('Usuário:',validators = [DataRequired()])
    password = PasswordField('Senha:', validators = [DataRequired()])
    password2 = PasswordField('Repita a senha:' ,validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')    

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Usuário ja registrado')

class NewEventForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    date_start = DateTimeLocalField('Inicio',validators=[DataRequired()], format = '%Y-%m-%dT%H:%M')
    date_end = DateTimeLocalField('Fim', validators=[DataRequired()], format = '%Y-%m-%dT%H:%M')
    description = TextAreaField()
    submit = SubmitField('Adicionar')

    def validate_date_end(self, date_end):
        event_start = self.date_start.data
        dayEvents = Event.query.filter(Event.event_owner == current_user.id).filter(Event.date_start < date_end.data).filter(Event.date_end  > date_end.data).first()
        
        if date_end.data < event_start:
            raise ValidationError('A data de termino não pode ser anterior a data de inicio')
        elif dayEvents is not None:
            raise ValidationError('Voce ja tem um evento marcado com essas datas')
    
    def validate_date_start(self, date_start):
    
        pendingEvents = Event.query.filter(Event.event_owner == current_user.id).filter(Event.date_start < date_start.data).filter(Event.date_end > date_start.data).first()
        event = Event.query.filter_by(date_start = date_start.data).first()
        if event is not None or pendingEvents is not None:
            raise ValidationError('Voce ja tem um evento marcado com essas datas')

class seachUser(FlaskForm):
    searchBar = StringField(validators=[])
    searchButton = SubmitField('Buscar')