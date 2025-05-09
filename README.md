# Chat Project – Secure Web Chat System

## Final Project – 11th Grade Cyber Security

Author: Eyal Raifler
School: De-Shalit High School, Rehovot, Israel

---

### Project Overview

This is a full-stack, secure, real-time web chat application inspired by WhatsApp. It supports user authentication, group and private messaging, media sharing, and a clean, responsive interface. The project was developed as a final cyber security assignment and demonstrates secure communication, database management, and real-time interaction via WebSockets.

---

### Features

#### Authentication

* User registration and login
* Guest access without sign-up

#### Messaging

* Real-time text communication via WebSockets
* Private and group chats
* Persistent chat history in a MySQL database

#### Media Sharing

* Support for image and file uploads
* Media preview in chat

#### Interface

* Responsive design for both desktop and mobile
* Single-page chat experience

---

### Technologies Used

| Layer       | Technologies                          |
| ----------- | ------------------------------------- |
| Frontend    | HTML, CSS, JavaScript                 |
| Backend     | Python (Flask, Flask-SocketIO)        |
| Database    | MySQL (with `mysql-connector-python`) |
| Development | VS Code, Chrome, MySQL Workbench      |

---

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/chat_project.git
   cd chat_project
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the database**

   * Create schema using `database/schema.sql`
   * Optionally load sample data with `database/seed.sql`

4. **Start the server**

   ```bash
   python run.py
   ```

5. **Access the chat app**
   Open in your browser: `http://127.0.0.1:5000`

---

### Security Considerations

* SQL injection prevention using parameterized queries
* Basic XSS protection (input sanitation)
* Planned implementation of hashed password storage
* Access control mechanisms for group management

---

### License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for more details.
