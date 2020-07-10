
from flask import Flask, render_template, request, redirect, url_for, Blueprint, make_response
from flask import current_app as app
from .. import forms
from datetime import datetime
from ..models import db, support_ticket

# Blueprint Configuration
tickets_bp = Blueprint(
    'tickets_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@tickets_bp.route('/', methods=['POST', 'GET'])
def dashboard():

    if request.method == 'POST':

        if request.form.get('search'):
            return redirect(f"/show_ticket/{request.form.get('search')}")

        if request.form.get('show_select') == 'all':
            return render_template('dashboard.html',all_tickets=support_ticket.query.all(),
                                   title="Ticket Support", show_selected="all",
                                   description="Web interface for support tickets")
        elif request.form.get('show_select') == 'Open':
            return render_template('dashboard.html',all_tickets=support_ticket.query.filter_by(status='Open').all(),
                                   title="Ticket Support",
                                   description="Web interface for support tickets", show_selected="Open")
        elif request.form.get('show_select') == 'Closed':
            return render_template('dashboard.html',all_tickets=support_ticket.query.filter_by(status='Closed').all(),
                                   title="Ticket Support",
                                   description="Web interface for support tickets", show_selected="Closed")



    return render_template('dashboard.html',all_tickets=support_ticket.query.all(),
                           title="Ticket Support",
                           description="Web interface for support tickets", show_selected="All")

@tickets_bp.route('/add', methods=['POST', 'GET'])
def add():
    form = forms.AddTicket()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_ticket = support_ticket(
                client=request.form.get('client'),
                issue=request.form.get('issue'),
                status=request.form.get('status'),
                assigned=request.form.get('assigned'),
                log=request.form.get('log'),
                deadline=request.form.get('deadline'),
                created=datetime.now(),
                last_update=datetime.now()
            )
            db.session.add(new_ticket)  # Adds new User record to database
            db.session.commit()  # Commits all changes

            return redirect(f"/show_ticket/?ticket={new_ticket.id}")


    return render_template('add.html',
                            title="Add Ticket", form=form)

@tickets_bp.route('/update')
def update():
    return render_template('update.html',
                            title="Update Ticket")

@tickets_bp.route('/show_ticket/', methods=['POST', 'GET'])
def show_ticket():
    id = request.args['ticket']
    return render_template(
        'show_tickets.html',
        ticket=support_ticket.query.filter_by(id=id).first(),
        title=f"Ticket | {id}"
    )

@tickets_bp.route('/edit_ticket/<id>', methods=['POST', 'GET'])
def edit_ticket(id):

    ticket = support_ticket.query.filter_by(id=id).first()

    form = forms.AddTicket()
    if request.method == 'POST':
        if form.validate_on_submit():
            client=request.form.get('client'),
            issue=request.form.get('issue'),
            status=request.form.get('status'),
            assigned=request.form.get('assigned'),
            log=request.form.get('log'),
            deadline=request.form.get('deadline'),
            last_update=datetime.now()


            ticket.client = client
            ticket.issue = issue
            ticket.status = status
            ticket.assigned = assigned
            ticket.log = log
            ticket.last_updated = last_update

            db.session.commit()  # Commits all changes

            return redirect(f"/show_ticket/?ticket={ticket.id}")

    form.client.data = ticket.client
    form.issue.data = ticket.issue
    form.status.data = ticket.status
    form.assigned.data = ticket.assigned
    form.deadline.data = ticket.deadline
    form.log.data = ticket.log

    return render_template('edit.html',
                            title="Edit Ticket", form=form, id=id)
