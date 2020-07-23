from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length
from .models import db, support_ticket, clients



class AddTicket(FlaskForm):

    client = SelectField('Client', [DataRequired()], coerce=int)
    client_name = StringField('Client Name')
    suite = StringField('Suite / PC')
    issue = StringField('Issue', [
        DataRequired()])
    log = TextAreaField('Ticket Log', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    status = SelectField('Status', [DataRequired()],
                        choices=[('Open', 'Open'),
                                 ('Closed', 'Closed'),
                                 ('Awaiting Action', 'Awaiting Action')])
    assigned = SelectField('Assign', [DataRequired()],
                        choices=[('Bob', 'Bob'),
                                 ('Toby', 'Toby'),
                                 ('Beth', 'Beth')])
    deadline = DateField('Deadline', [
        DataRequired()], format='%Y-%m-%d')
    urgency = SelectField('Urgency', [DataRequired()],
                        choices=[('High', 'High'),
                                 ('Low', 'Low')])

    submit = SubmitField('Submit')


class EditTicket(FlaskForm):

    client = SelectField('Client', [DataRequired()], coerce=int)
    client_name = StringField('Client Name')
    suite = StringField('Suite / PC')
    issue = StringField('Issue', [
        DataRequired()])
    status = SelectField('Status', [DataRequired()],
                        choices=[('Open', 'Open'),
                                 ('Closed', 'Closed'),
                                 ('Awaiting Action', 'Awaiting Action')])
    assigned = SelectField('Assign', [DataRequired()],
                        choices=[('Bob', 'Bob'),
                                 ('Toby', 'Toby'),
                                 ('Beth', 'Beth')])
    deadline = DateField('Deadline', [
        DataRequired()], format='%Y-%m-%d')
    urgency = SelectField('Urgency', [DataRequired()],
                        choices=[('High', 'High'),
                                 ('Low', 'Low')])

    submit = SubmitField('Submit')

class EditLog(FlaskForm):
    log = TextAreaField('Ticket Log', [
        DataRequired()])

    submit = SubmitField('Submit')


class UpdateTicket(FlaskForm):
    log = TextAreaField('Ticket Log', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    status = SelectField('Status', [DataRequired()],
                        choices=[('Open', 'Open'),
                                 ('Closed', 'Closed'),
                                 ('Awaiting Action', 'Awaiting Action')])
    assigned = SelectField('Assign', [DataRequired()],
                        choices=[('Bob', 'Bob'),
                                 ('Toby', 'Toby'),
                                 ('Beth', 'Beth')])
    deadline = DateField('Deadline', [
        DataRequired()], format='%Y-%m-%d')
    urgency = SelectField('Urgency', [DataRequired()],
                        choices=[('High', 'High'),
                                 ('Low', 'Low')])

    submit = SubmitField('Submit')


class AddClient(FlaskForm):
    """Contact form."""
    client = StringField('Client', [
        DataRequired()])
    submit = SubmitField('Submit')
