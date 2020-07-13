from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length


class AddTicket(FlaskForm):
    """Contact form."""
    client = StringField('Client', [
        DataRequired()])
    issue = StringField('Issue', [
        DataRequired()])
    log = TextAreaField('Ticket Log', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    status = SelectField('Assign', [DataRequired()],
                        choices=[('Open', 'Open'),
                                 ('Closed', 'Closed'),
                                 ('Awaiting Action', 'Awaiting Action')])
    assigned = SelectField('Assign', [DataRequired()],
                        choices=[('Bob', 'Bob'),
                                 ('Toby', 'Toby'),
                                 ('Beth', 'Beth')])
    deadline = TextField('Deadline', [
        DataRequired()])

    submit = SubmitField('Submit')

class AddClient(FlaskForm):
    """Contact form."""
    client = StringField('Client', [
        DataRequired()])
    submit = SubmitField('Submit')
