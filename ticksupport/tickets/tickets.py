
from flask import Flask, render_template, request, redirect, url_for, Blueprint, make_response
from flask import current_app as app
from .. import forms
from datetime import datetime, date
from ..models import db, support_ticket, clients

USER = "Bob"

# Blueprint Configuration
tickets_bp = Blueprint(
    'tickets_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


"""def log_input(text_input, previous_message=None):
    print(previous_message)
    log_split = []

    if previous_message != None:

        if '## EDITED' in previous_message:
            log_split.append(previous_message.split('## EDITED')[0])
            try:
                log_split.append(text_input.split('|', 1)[1])
            except IndexError:
                log_split.append(text_input)
        else:

            log_split = text_input.split('|', 1)
            if len(log_split) == 2:
                log_split[0] = previous_message.split('@')[0]
            else:
                log_split = [str(previous_message.split('|', 1)[0]), str(log_split[0])]

        log_entry = f"{log_split[0]} ## EDITED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{USER} | {log_split[1]}\n"

    else:
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{USER} | {text_input}\n"


    return log_entry"""

def log_input(text_input, ticket=None, entry_type=0):
    # except a text input and create a time stamp and user # NOTE
    # make a tuple of the two and either append it onto a list
    # Or replace the edited entry with new edit and updated time stamp

    # If new entry
    if entry_type == 0:
        # New log
        ticket_log = []
        time_stamp = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{USER} | "
        full_entry = [time_stamp, text_input + '\n']

    elif entry_type == 1:
        # If entry is an update
        ticket_log = eval(ticket)
        time_stamp = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{USER} | "
        full_entry = [time_stamp, text_input + '\n']

    elif entry_type == 2:
        # If entry type is an edit
        ticket_log = eval(ticket)

        original_log = []

        # Split text into lines
        all_messages = []


        all_lines = text_input.split('\n')

        # Split out all messages only
        for line in all_lines:
            try:
                all_messages.append(line.split('|')[1])
            except IndexError:
                pass

        # Get message only
        for log in ticket_log:
            original_log.append(log[1])

        edits = []

        # Find edits and save location
        for i in range(len(original_log)):
            if original_log[i].lstrip() != all_messages[i].lstrip():
                print(original_log[i])
                print(all_messages[i])
                edits.append(i)


        for i in edits:
            ticket_log[i][1] = all_messages[i]
            if '## EDITED' in ticket_log[i][0]:
                original_timestamp = ticket_log[i][0].split('## EDITED')[0]
                new_timestamp = f"## EDITED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{USER} | "
            else:
                original_timestamp = ticket_log[i][0].split('|')[0]
                new_timestamp = f"## EDITED {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{USER} | "

            ticket_log[i][0] = original_timestamp + new_timestamp

        return ticket_log


    ticket_log.append(full_entry)

    return ticket_log






@tickets_bp.route('/', methods=['POST', 'GET'])
def dashboard():

    if request.method == 'POST':

        if request.form.get('search'):
            return redirect(f"/show_ticket/{request.form.get('search')}")

        assigned = request.form.get('show_assigned')
        status = request.form.get('show_status')
        client_select = request.form.get("show_clients")
        urgency_filter = ""
        filter_code = 0
        search_filter = ""

        if assigned == 'All' and status == 'All' and client_select == 'All Clients':
            return render_template('dashboard.html',all_tickets=support_ticket.query.order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all(),
                                    clients=clients.query.all(), title="Ticket Support", header=f"All", show_status="All", show_assigned="All",
                                   description="Web interface for support tickets",  show_clients=client_select, now=date.today())

        print("assigned:  " + assigned +'|')
        print("status:  " + status+'|')
        print("client:  " + client_select+'|')

        if assigned == 'All':
            filter_code+= 1

        if status == 'All':
            filter_code+= 3

        if client_select == 'All Clients':
            filter_code+= 5

        print(filter_code)


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

        print(search_filter)

        return render_template('dashboard.html', all_tickets=search_filter,  clients=clients.query.all(),  show_clients=client_select,
                                   title="Ticket Support", now=date.today(),
                                   description="Web interface for support tickets", header=f"{assigned} : {status}", show_status=f"{status}", show_assigned=f"{assigned}")


    return render_template('dashboard.html',all_tickets=support_ticket.query.filter_by(status='Open').order_by(support_ticket.deadline.asc()).order_by(support_ticket.urgency.asc()).all(),
                           clients=clients.query.all(), title="Ticket Support", now=date.today(),
                           description="Web interface for support tickets", header='All Open', show_clients='All Clients', show_status="Open", show_assigned="All")

@tickets_bp.route('/add', methods=['POST', 'GET'])
def add():
    form = forms.AddTicket()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_ticket = support_ticket(
                client=request.form.get('client'),
                client_name=request.form.get('client_name'),
                suite=request.form.get('suite'),
                issue=request.form.get('issue'),
                status=request.form.get('status'),
                assigned=request.form.get('assigned'),
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
def show_ticket():
    id = request.args['ticket']
    ticket = support_ticket.query.filter_by(id=id).first()
    log = eval(ticket.log)
    return render_template(
        'show_tickets.html',
        ticket=ticket,
        title=f"Ticket | {id}", ticket_log=log)

@tickets_bp.route('/edit_ticket/<id>', methods=['POST', 'GET'])
def edit_ticket(id):

    ticket = support_ticket.query.filter_by(id=id).first()
    print(ticket)

    form = forms.AddTicket()
    if request.method == 'POST':
        if form.validate_on_submit():
            client=request.form.get('client'),
            client_name = request.form.get('client_name')
            suite=request.form.get('suite')
            issue=request.form.get('issue'),
            status=request.form.get('status'),
            urgency=request.form.get('urgency'),
            assigned=request.form.get('assigned'),
            log=str(log_input(request.form.get('log')+'\n', ticket=ticket.log, entry_type=2)),
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
            ticket.log = log
            ticket.last_update = last_update

            db.session.commit()  # Commits all changes

            return redirect(f"/show_ticket/?ticket={ticket.id}")

    form.client.data = ticket.client
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
        text_entry = entry[0] + entry[1]
        text_log.append(text_entry)

    form.log.data = "".join(text_log)
    #form.process()

    return render_template('edit.html',
                            title="Edit Ticket", form=form, id=id, client_choice=ticket.client)



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


@tickets_bp.route('/update_ticket/<id>', methods=['POST', 'GET'])
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
