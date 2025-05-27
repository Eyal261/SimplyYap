from flask import Flask, request, jsonify, render_template, redirect, session
from users import create_user, verify_password, update_user_profile_picture
from flask_socketio import SocketIO, send, join_room, leave_room, emit
import threading
import webbrowser
from groups import get_user_groups, create_group, add_user_to_group, remove_user_from_group, is_user_in_group, get_group_members
from chat import save_message, get_messages_for_group
import os
from werkzeug.utils import secure_filename
import time
from mailer import send_contact_mail


app = Flask(__name__)
app.secret_key = 'super_secret_key_123456'
socketio = SocketIO(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['FILE_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'files')
os.makedirs(app.config['FILE_UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return jsonify({"error": "Missing username or password or email"}), 400
    
    try:
        user_id = create_user(username, password, email)
        session['username'] = username
        session['user_id'] = user_id
        return jsonify({"message": "User created", "user id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.json
    print("[LOGIN] Data received:", data)
    username = data.get("username")
    password = data.get("password")

    user = verify_password(username, password)
    if user:
        session['username'] = username
        session['user_id'] = user.user_id
        print("[LOGIN] success for:", username)
        return jsonify({"message": "Login successful", "user id": user.user_id}), 200
    else:
        print("[LOGIN] Failed for:", username)
        return jsonify({"error": "Invalid credentials"}), 401

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@socketio.on('group_message')
def handle_group_data(data):
    print("[SocketIO] Message received:", data)
    group_id = data.get('group')

    # Save the message to the database
    message_content = data.get('text') or data.get('content') # Use 'text' for text messages, 'content' for file/image
    message_id = save_message(
        sender_id=data.get('user_id'),
        content=message_content,
        group_id=group_id,
        message_type=data.get('message_type'),
        file_name=data.get('file_name')
    )

    # Optionally attach message_id before sending
    data['message_id'] = message_id

    # Broadcast to everyone in the group
    emit('group_message', data, to=str(group_id))



@app.route('/profile_pic', methods=['GET', 'POST'])
def profile_pic():
    user_id = session.get('user_id')
    username = session.get('username')

    if not user_id:
        return redirect('/login')

    if request.method == 'POST':
        image_choice = request.form.get('image_choice')

        if image_choice and image_choice.startswith('profile_pic'):
            image_path = f'default_profile_pictures/{image_choice}'

        elif image_choice == 'upload' and 'custom_image' in request.files:
            file = request.files['custom_image']
            if file and file.filename.strip() != '':
                filename = secure_filename(file.filename)
                timestamp = int(time.time())
                unique_filename = f"user_{user_id}_{timestamp}_{filename}"

                upload_folder = os.path.join(basedir, "static", "uploaded_profile_pictures")
                os.makedirs(upload_folder, exist_ok=True)

                save_path = os.path.join(upload_folder, unique_filename)
                file.save(save_path)

                image_path = f"uploaded_profile_pictures/{unique_filename}"  # ✅ Relative to /static
            else:
                return "No file uploaded", 400
        else:
            return "Invalid image selection", 400

        # Save to database
        try:
            update_user_profile_picture(user_id, image_path)
            session['profile_picture'] = image_path  # Update session with new profile picture path
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return redirect('/chat')

    return render_template('profile_pic.html', username=username, user_id=user_id)


    
    
    


@app.route('/chat')
def chat():
    username = session.get('username')
    user_id = session.get('user_id')
    print("----------------------------------------------------")
    print(f"User ID: {user_id}, Username: {username}, Profile Picture: {session.get('profile_picture')}")
    profile_picture = session.get('profile_picture') or 'default_profile_pictures/profile_pic1.png'
    
    if not username:
        return redirect('/login')
    return render_template('chat.html', username=username, user_id=user_id, profile_picture=profile_picture)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        send_contact_mail(name, email, message)

        return render_template('contact.html', submitted=True)
    return render_template('contact.html', submitted=False)



@app.route('/groups', methods=['GET'])
def my_groups():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    groups = get_user_groups(user_id)
    print(f"Groups: {groups}")
    return jsonify(groups)

@app.route('/create_group', methods=['POST'])
def api_create_group():
    data = request.json
    group_name = data.get('group_name')
    creator_id = session.get('user_id')
    print(f"Creating group: {group_name} with creator id: {creator_id}")
    if not group_name or not creator_id:
        return jsonify({"error": "Missing group name or user id"}), 400
    try:
        group_id = create_group(group_name, creator_id)
        return jsonify({"message": "Group created", "group_id": group_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@socketio.on('join_group_socket')
def handle_join_group_socket(group_id):
    join_room(str(group_id))
    print(f"Joined socket room: {group_id}")

@app.route('/messages/<int:group_id>')
def get_messages(group_id):
    messages = get_messages_for_group(group_id)
    print(f"Messages for group {group_id}: {messages}")
    return jsonify(messages) 

@app.route('/join_group', methods=['POST'])
def join_group():
    data = request.json
    group_id = data.get('group_id')
    user_id = session.get('user_id')
    if not group_id or not user_id:
        return jsonify({"error": "Missing group id or user id"}), 400
    is_user_in_group_result = is_user_in_group(group_id, user_id)
    if is_user_in_group_result:
        return jsonify({"error": "User already in group"}), 400
    is_admin = data.get('is_admin', False)
    print(f"Joining group {group_id} as user {user_id} with admin status {is_admin}")
    add_user_to_group(group_id, user_id, is_admin)
    return jsonify({'message': 'Joined group successfully'})


@app.route('/delete_group', methods=['POST'])
def leave_group():
    data = request.json
    group_id = data.get('group_id')
    user_id = session.get('user_id')
    if not group_id or not user_id:
        return jsonify({"error": "Missing group id or user id"}), 400
    if not is_user_in_group(group_id, user_id):
        return jsonify({"error": "User not in group"}), 400
    remove_user_from_group(group_id, user_id)
    return jsonify({"message": "Deleted group successfully"})


@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        group_id = request.args.get('group_id') or "common"

        # Use timestamp to avoid overwrites
        timestamp = int(time.time())
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_{timestamp}{ext}"

        group_folder = os.path.join(app.config['FILE_UPLOAD_FOLDER'], str(group_id))
        os.makedirs(group_folder, exist_ok=True)

        file_path = os.path.join(group_folder, new_filename)
        file.save(file_path)

        file_url = f"/static/files/{group_id}/{new_filename}"
        return jsonify({
            'file_url': file_url,
            'file_name': file.filename
            }), 200

    return jsonify({'error': 'No file part'}), 400


@app.route('/return_all_group_members', methods=['POST'])
def return_all_group_members():
    if not session.get('user_id'):
        return jsonify({"error": "User not logged in"}), 401
    data = request.json
    group_id = data.get('group_id')
    user_id = session.get('user_id')
    return jsonify({"Group_members: ": get_group_members(group_id)})






if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    

