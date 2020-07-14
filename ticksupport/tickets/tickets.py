
from flask import Flask, render_template, request, redirect, url_for, Blueprint, make_response
from flask import current_app as app
from .. import forms
from datetime import datetime
from ..models import db, support_ticket, clients

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

        assigned = request.form.get('show_assigned')
        status = request.form.get('show_status')

        if assigned == 'All' and status == 'All':
            return render_template('dashboard.html',all_tickets=support_ticket.query.all(),
                                   title="Ticket Support", header=f"{assigned} : {status}", show_status="All", show_assigned="All",
                                   description="Web interface for support tickets")
        elif status == 'All':
            return render_template('dashboard.html',all_tickets=support_ticket.query.filter_by(assigned=assigned).all(),
                                   title="Ticket Support",
                                   description="Web interface for support tickets", header=f"{assigned} : {status}", show_status=f"{status}", show_assigned=f"{assigned}")
        elif assigned == 'All':
            return render_template('dashboard.html',all_tickets=support_ticket.query.filter_by(status=status).all(),
                                   title="Ticket Support",
                                   description="Web interface for support tickets", header=f"{assigned} : {status}", show_status=f"{status}", show_assigned=f"{assigned}")
        else:
            return render_template('dashboard.html',all_tickets=support_ticket.query.filter_by(status=status, assigned=assigned).all(),
                                   title="Ticket Support",
                                   description="Web interface for support tickets", header=f"{assigned} : {status}", show_status=f"{status}", show_assigned=f"{assigned}")


    return render_template('dashboard.html',all_tickets=support_ticket.query.all(),
                           clients=clients.query.all(), title="Ticket Support",
                           description="Web interface for support tickets", header='All', show_clients='All Clients', show_status="All", show_assigned="All")

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
                last_update=datetime.now(),
                urgency=request.form.get('urgency'),
                created_by='Bob' #Replace with user_name varible after user function added

            )
            db.session.add(new_ticket)  # Adds new User record to database
            db.session.commit()  # Commits all changes

            return redirect(f"/show_ticket/?ticket={new_ticket.id}")


    return render_template('add.html',
                            title="Add Ticket", form=form)


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
    print(ticket)

    form = forms.AddTicket()
    if request.method == 'POST':
        if form.validate_on_submit():
            client=request.form.get('client'),
            issue=request.form.get('issue'),
            status=request.form.get('status'),
            urgency=request.form.get('urgency'),
            assigned=request.form.get('assigned'),
            log=request.form.get('log'),
            deadline=request.form.get('deadline'),
            last_update=datetime.now()


            ticket.client = client
            ticket.issue = issue
            ticket.status = status
            ticket.urgency = urgency
            ticket.assigned = assigned
            ticket.log = log
            ticket.last_updated = last_update

            db.session.commit()  # Commits all changes

            return redirect(f"/show_ticket/?ticket={ticket.id}")

    form.client.data = ticket.client
    form.issue.data = ticket.issue
    form.status.data = ticket.status
    form.urgency.data = ticket.urgency
    form.assigned.data = ticket.assigned
    form.deadline.data = ticket.deadline
    form.log.data = ticket.log

    return render_template('edit.html',
                            title="Edit Ticket", form=form, id=id)



@tickets_bp.route('/add_client', methods=['POST', 'GET'])
def add_client():
    form = forms.AddClient()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_client = clients(
                client=request.form.get('client'),
            )
            db.session.add(new_client)  # Adds new User record to database
            db.session.commit()  # Commits all changes

            return render_template('add_client.html',
                                    title="Add Client", form=form, all_clients=clients.query.all())


    return render_template('add_client.html',
                            title="Add Client", form=form, all_clients=clients.query.all())
