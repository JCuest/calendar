import os
from app import app, db
from flask import render_template, redirect
from app.forms import LoginForm, RegistrationForm, NewEventForm, seachUser
from flask import send_from_directory, flash, request
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User, Event, RelationUsers, FriendRequest
from datetime import datetime

''' USER FUNCTION   '''
def friendList( user_id):
    rel_u1 = RelationUsers.query.filter_by(user1 = user_id).all()
    rel_u2 = RelationUsers.query.filter_by(user2 = user_id).all()
    f1 = []
    f2 = []

    for i in rel_u1:
        f1 += [User.query.filter_by(id = i.user2).first()]
        
    for j in rel_u2:
        f2 += [User.query.filter_by(id = j.user1).first()]
        
    friends = f1 + f2
        
    return friends

def isFriend(user_id, target_id):
    f1 = RelationUsers.query.filter_by(user1 = user_id).filter_by(user2=target_id).first()
    f2 = RelationUsers.query.filter_by(user2 = user_id).filter_by(user1=target_id).first()

    if f1 is not None or f2 is not None:
        return True
    return False 

def commonFriendList(user_id, target_id):
    f1 = friendList(user_id)
    f2 = friendList(target_id)

    mutual = list(set(f1).intersection(f2))
    return mutual

def isInvited(user_id, target_id):
    req = FriendRequest.query.filter_by(user1 = user_id).filter_by(user2 = target_id).first()
    qer = FriendRequest.query.filter_by(user1 = target_id).filter_by(user2 = user_id).first()
    if req is not None and qer is None:
        return 1
    elif req is None and qer is not None:
        return 2

    return 0

''' ------ '''
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/' )
@app.route('/home')
def home():
    return render_template('home.html') 

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Usuário ou Senha incorretos") 
            return redirect('/login')
        login_user(user)
        return redirect('/home')
    return render_template('login.html', form = form)
    
@app.route('/logout')
def user_logout():
    logout_user()
    return redirect('/home')

@app.route('/register', methods=['GET','POST'])
def user_new():
    if current_user.is_authenticated:
        return redirect('/home')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, password = form.password2.data)
        db.session.add(user)
        db.session.commit()
        flash('Bem vindo ao TokenCalendar!!')
        return redirect('/login')
    return render_template('register.html', form = form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    friend = isFriend(current_user.id, user.id)
    commonF = commonFriendList(current_user.id, user.id)
    invSend = isInvited(current_user.id, user.id)
    return render_template('user.html', user=user, friend = friend, commonF = commonF, invSend = invSend)


@app.route('/event')
@login_required
def event_page():
    user = User.query.filter_by(username = current_user.username).first()
    nextEvent = Event.query.filter(Event.event_owner == user.id).filter(Event.date_start > datetime.now()).order_by(Event.date_start.desc()).all()
    pastEvent = Event.query.filter(Event.event_owner == user.id).filter(Event.date_start < datetime.now()).order_by(Event.date_start.desc()).all()
    return render_template('event.html', user=user, nextEvent=nextEvent, pastEvent = pastEvent)

@app.route('/event/new', methods=['GET','POST'])
@login_required
def event_new_page(): 
    form_event = NewEventForm()

    if form_event.validate_on_submit():
        user = User.query.filter_by(username = current_user.username).first()
        event = Event(title = form_event.title.data, description = form_event.description.data, date_start = form_event.date_start.data, date_end = form_event.date_end.data, event_owner = user.id )
        db.session.add(event)
        db.session.commit()
        return redirect('/event')
        
    return render_template('new_event.html', form=form_event)


@app.route('/event/<event_id>')
@login_required
def event_view(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()
    user = User.query.filter_by(id = event.event_owner).first()
    dateNow = datetime.now()
    friends = friendList(current_user.id)

    return render_template('event_view.html', event=event, user=user, dateNow = dateNow, friends = friends)

@app.route('/edit/<event_id>' , methods=['GET', 'POST'])
@login_required
def event_editor(event_id):

    event = Event.query.get(event_id)
    form = NewEventForm()

    if request.method == 'GET':
        form.title.data = event.title
        form.date_start.data = event.date_start
        form.date_end.data = event.date_end
        form.description.data = event.description    

    if form.validate_on_submit() and form.validate_date():
        event.title = form.title.data  
        event.date_start = form.date_start.data  
        event.date_end = form.date_end.data  
        event.description = form.description.data
        db.session.commit()
        return redirect('/event')

    return render_template('event_editor.html', event = event, form=form)


@app.route('/delete/<event_id>')
@login_required
def event_delete(event_id):
    event = Event.query.get(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect('/event')

@app.route('/friend', methods=['GET','POST'])
@login_required
def user_friends():
    search = seachUser()
    invitFriend = FriendRequest.query.filter_by(user2 = current_user.get_id()).all()
    requestFriend = []
    commonFriends = {}

    if search.validate_on_submit():
        name = search.searchBar.data
        user = User.query.filter_by(username = name).first()
    
        return redirect('/user/' + user.username)

    for k in invitFriend:
        requestFriend += [User.query.filter_by(id = k.user1).first()]

    for j in requestFriend:
        commonFriends[j.id] = len(commonFriendList(current_user.id, j.id))

    friends = friendList(current_user.id)

    return render_template('friend.html', friends = friends, requestFriend = requestFriend, commonFriends = commonFriends, search = search)

@app.route('/invite/<user_id>')
@login_required
def invite_new_friend(user_id):
    user = User.query.filter_by(id = user_id).first()
    user_name = user.username
    req = FriendRequest(user1 = current_user.get_id(), user2 = user_id)
    db.session.add(req)
    db.session.commit()
    return redirect('/user/' + user_name)

@app.route('/acept/<sender_id>')
@login_required
def acept_friend_request(sender_id):
    friends = RelationUsers(user1 = current_user.get_id(), user2 = sender_id)
    req = FriendRequest.query.filter_by(user1 = sender_id).filter_by(user2 = current_user.get_id()).first()

    db.session.add(friends)
    db.session.delete(req)

    db.session.commit()
    return redirect('/friend')

@app.route('/cancel/<sender_id>')
@login_required
def cancel_friend_request(sender_id):
    req = FriendRequest.query.filter_by(user1 = sender_id).filter_by(user2 = current_user.get_id()).first()
    db.session.delete(req)
    db.session.commit()
    return redirect('/friend')
