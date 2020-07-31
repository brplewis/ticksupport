
from flask import Flask, render_template, request, redirect, url_for, Blueprint, make_response
from flask_login import current_user, login_required
from flask import current_app as app
from .. import forms
from .. import auth
from datetime import datetime, date
from ..models import db, support_ticket, clients, User
from flask_login import logout_user
from .. import login_manager

# Blueprint Configuration
tickets_bp = Blueprint(
    'tickets_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


print(auth.USER_ID)

@app.context_processor
def insert_user():
    if auth.USER_ID == None:
        return dict(user='No User')
    else:
        id = int(auth.USER_ID)
        user = User.query.get(id)
        return dict(user=user.name)


@app.context_processor
def if_admin():
    if auth.USER_ID == None:
        return dict(admin=False)
    else:
        user = User.query.get(auth.USER_ID)
        if user.account_type == 'admin':
            return dict(admin=True)
        else:
            return dict(admin=False)



def log_input(text_input, ticket=None, entry_type=0, log_id=None):
    # except a text input and create a time stamp and user # NOTE
    # make a tuple of the two and either append it onto a list
    # Or replace the edited entry with new edit and updated time stamp

    # If new entry
    if entry_type == 0:
        # New log
        ticket_log = []
        time_stamp = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{auth.USER} | "
        full_entry = [time_stamp, text_input + '\n']

    elif entry_type == 1:
        # If entry is an update
        ticket_log = eval(ticket)
        time_stamp = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{auth.USER} | "
        full_entry = [time_stamp, text_input + '\n']

    elif entry_type == 2:
        ticket_log = eval(ticket)

        log_id = int(log_id)

        ticket_log[log_id][1] = text_input

        if '## EDITED' in ticket_log[log_id][0]:
            original_timestamp = ticket_log[log_id][0].split('## EDITED')[0]
            new_timestamp = f"## EDITED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{auth.USER} | "
        else:
            original_timestamp = ticket_log[log_id][0].split('|')[0]
            new_timestamp = f"## EDITED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{auth.USER} | "

        ticket_log[log_id][0] = original_timestamp + new_timestamp

        return ticket_log

    ticket_log.append(full_entry)

    return ticket_log


@tickets_bp.route('/', methods=['POST', 'GET'])
@login_required
def dashboard():

    client_list = [(0, 'All Clients')]
    for client in clients.query.all():
        client_list.append((client.id, client.client))

    assigned_list = [(0, 'All Users')]
    for assigned in User.query.all():
        assigned_list.append((assigned.id, assigned.name))

    form = forms.DashboardSearch()
    form.client.choices = client_list
    form.assigned.choices = assigned_list



    if request.method == 'POST':

        if request.form.get('search'):
            return redirect(f"/show_ticket/{request.form.get('search')}")

        assigned = dict(form.assigned.choices).get(form.assigned.data)
        status = request.form.get('status')
        client_select = dict(form.client.choices).get(form.client.data)
        urgency_filter = ""
        filter_code = 0
        search_filter = ""

        form.client.default = client_select

        if assigned == 'All' and status == 'All' and client_select == 'All Clients':
            return render_template('dashboard.html',all_tickets=support_ticket.query.order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all(),
                                    clients=clients.query.all(), title="Ticket Support", header=f"All", show_status="All", show_assigned="All",
                                   description="Web interface for support tickets",  show_clients=client_select, now=date.today())


        if assigned == 'All Users':
            filter_code+= 1

        if status == 'All':
            filter_code+= 3

        if client_select == 'All Clients':
            filter_code+= 5


        if filter_code == 1:
            search_filter = support_ticket.query.filter_by(client=client_select, status=status).order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all()
        elif filter_code == 3:
            search_filter = support_ticket.query.filter_by(client=client_select, assigned=assigned).order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all()
        elif filter_code == 4:
            search_filter = support_ticket.query.filter_by(client=client_select).order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all()
        elif filter_code == 5:
            search_filter = support_ticket.query.filter_by(assigned=assigned, status=status).order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all()
        elif filter_code == 6:
            search_filter = support_ticket.query.filter_by(status=status).order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all()
        elif filter_code == 8:
            search_filter = support_ticket.query.filter_by(assigned=assigned).order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all()
        elif filter_code == 9:
            search_filter = support_ticket.query.order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all()
        elif filter_code == 0:
            search_filter = support_ticket.query.filter_by(client=client_select, assigned=assigned, status=status).order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all()

        return render_template('dashboard.html', all_tickets=search_filter,  clients=clients.query.all(),  show_clients=client_select,
                                   title="Ticket Support", now=date.today(), form=form,
                                   description="Web interface for support tickets", header=f"{assigned} : {status}", show_status=f"{status}", show_assigned=f"{assigned}")


    return render_template('dashboard.html',all_tickets=support_ticket.query.filter_by(status='Open').order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all(),
                           title="Ticket Support", now=date.today(), form=form,
                           description="Web interface for support tickets", header='All Open', show_clients='All Clients', show_status="Open", show_assigned="All")

@tickets_bp.route('/add', methods=['POST', 'GET'])
@login_required
def add():

    client_list=[(client.id, client.client) for client in clients.query.all()]
    assigned_list=[(user.id, user.name) for user in User.query.all()]
    form = forms.AddTicket()
    form.client.choices = client_list
    form.assigned.choices = assigned_list
    if request.method == 'POST':
        if form.validate_on_submit():
            new_ticket = support_ticket(
                #client = dict(form.client.choices).get(form.client.data),
                client = str((request.form.get('client'), dict(form.client.choices).get(form.client.data))),
                client_name=request.form.get('client_name'),
                suite=request.form.get('suite'),
                issue=request.form.get('issue'),
                status=request.form.get('status'),
                assigned=dict(form.assigned.choices).get(form.assigned.data),
                log=str(log_input(request.form.get('log'), entry_type=0)),
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
@login_required
def show_ticket():
    id = request.args['ticket']
    ticket = support_ticket.query.filter_by(id=id).first()
    log = eval(ticket.log)
    client = eval(ticket.client)
    return render_template(
        'show_tickets.html',
        ticket=ticket, id=id, client=client[1]
        title=f"Ticket | {id}", ticket_log=log)

@tickets_bp.route('/edit_ticket/<id>', methods=['POST', 'GET'])
@login_required
def edit_ticket(id):

    ticket = support_ticket.query.filter_by(id=id).first()
    client_list=[(client.id, client.client) for client in clients.query.all()]
    assigned_list=[(user.id, user.name) for user in User.query.all()]
    client_id = eval(ticket.client)[0]
    form = forms.EditTicket(client=client_id)
    form.client.choices = client_list
    form.assigned.choices = assigned_list

    if request.method == 'POST':
        if form.validate_on_submit():
            client = dict(form.client.choices).get(form.client.data)
            #client=request.form.get('client'),
            client_name = request.form.get('client_name')
            suite=request.form.get('suite')
            issue=request.form.get('issue'),
            status=request.form.get('status'),
            urgency=request.form.get('urgency'),
            assigned=dict(form.assigned.choices).get(form.assigned.data),
            deadline=request.form.get('deadline'),
            last_update=datetime.now()


            ticket.client = client
            ticket.client_name = client_name
            ticket.suite = suite
            ticket.issue = issue
            ticket.status = status
            ticket.urgency = urgency
            ticket.assigned = assigned
            ticket.deadline = deadline
            ticket.last_update = last_update

            db.session.commit()  # Commits all changes

            return redirect(f"/show_ticket/?ticket={ticket.id}")

    client_selected = (f'{id}', f'{ticket.client}')

    form.client_name.data = ticket.client_name
    form.suite.data = ticket.suite
    form.issue.data = ticket.issue
    form.status.data = ticket.status
    form.urgency.data = ticket.urgency
    form.assigned.data = ticket.assigned
    form.deadline.data = ticket.deadline

    text_log = []
    log = eval(ticket.log)
    for entry in log:
        text_log.append(entry[1])

    return render_template('edit.html',
                            title="Edit Ticket", form=form, id=id, ticket_log=log, client=client_selected)

@tickets_bp.route('/edit_log/<id>_<log_id>', methods=['POST', 'GET'])
@tickets_bp.route('/show_ticket/edit_log/<id>_<log_id>', methods=['POST', 'GET'])
@login_required
def edit_log(id, log_id):
    form = forms.EditLog()
    ticket = support_ticket.query.filter_by(id=id).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            log=str(log_input(request.form.get('log'), ticket=ticket.log, entry_type=2, log_id=log_id)),
            last_update=datetime.now()



            ticket.log = log
            ticket.last_update = last_update

            db.session.commit()  # Commits all changes

            return redirect(f"/show_ticket/?ticket={ticket.id}")


    log = eval(ticket.log)

    log_to_edit = log[int(log_id)]

    form.log.data = log_to_edit[1]

    client = eval(ticket.client)


    return render_template(
        'edit_log.html',
        ticket=ticket, id=id, client=client[1],
        title=f"Ticket | {id}", log_to_edit=log_to_edit, form=form, ticket_log=log, log_id=log_id)




@tickets_bp.route('/add_client', methods=['POST', 'GET'])
@login_required
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


@tickets_bp.route('/update_ticket/<id>', methods=['POST', 'GET'])
@login_required
def update_ticket(id):

    ticket = support_ticket.query.filter_by(id=id).first()
    print(ticket)

    form = forms.UpdateTicket()
    if request.method == 'POST':
        print("POSTED")
        if form.validate_on_submit():
            print("SUBMITTED")
            status=request.form.get('status'),
            assigned=request.form.get('assigned'),
            urgency=request.form.get('urgency'),
            log=str(log_input(request.form.get('log'), ticket=ticket.log, entry_type=1)),
            deadline=request.form.get('deadline'),
            last_update=datetime.now()
            print(type(log))


            ticket.status = status
            ticket.urgency = urgency
            ticket.assigned = assigned
            ticket.deadline = deadline
            ticket.log = log
            ticket.last_update = last_update

            db.session.commit()  # Commits all changes

            return redirect(f"/show_ticket/?ticket={ticket.id}")

    form.status.data = ticket.status
    form.urgency.data = ticket.urgency
    form.assigned.data = ticket.assigned
    form.deadline.data = ticket.deadline


    return render_template('update.html',
                            title=f"Ticket {ticket.id}", form=form, id=id, client_choice=ticket.client, ticket=ticket)

@tickets_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
