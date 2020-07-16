from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length
from .models import db, support_ticket, clients



class AddTicket(FlaskForm):
    """Contact form."""
    """client = QuerySelectField(
        u'Client',
        query_factory= all_clients, get_pk=lambda x: x.client, get_label='client',
        allow_blank=False
    )"""

    client = SelectField('Client', [DataRequired()],
                        choices=[(client.client, client.client) for client in clients.query.all()])
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

class AddClient(FlaskForm):
    """Contact form."""
    client = StringField('Client', [
        DataRequired()])
    submit = SubmitField('Submit')
