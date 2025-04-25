# 💬 Chat Project – Secure Web Chat System

A full-stack, secure, real-time web chat system inspired by WhatsApp. Built as a final Cyber Security project by Eyal Raifler (11th grade, De-Shalit High School, Rehovot, Israel), the system supports private and group messaging, media uploads, and anonymous guest access.

---

## 🚀 Features

### 🔐 Authentication
- User registration and login with password verification
- Guest access (no signup required)

### 💬 Messaging
- Real-time messaging with WebSockets
- Private and group chats
- Automatic chat refresh without page reload
- Chat history stored in a database

### 📁 Media
- Upload and share images and voice messages
- Media preview in chat window

### 🧠 AI Assistant (Coming Soon)
- Optional built-in assistant to help with phrasing and more

### 📱 UI/UX
- Clean responsive web interface (works on desktop & mobile)
- Single page layout (like WhatsApp)

---

## 🛠️ Tech Stack

| Layer        |  Tools / Languages                         |
|--------------|--------------------------------------------|
| Frontend     | HTML, CSS, JavaScript                      |
| Backend      | Python, Flask, Flask-SocketIO              |
| Database     | MySQL (accessed via mysql-connector)       |
| Hosting/Test | VS Code, Chrome, Terminal, MySQL Workbench |

---

## 🗃️ File Structure

```
chat_project/
├── client/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── media/
├── server/
│   ├── app.py
│   ├── auth.py
│   ├── chat.py
│   ├── socket_handler.py
│   ├── db/
│   └── uploads/
├── database/
│   ├── schema.sql
│   └── seed.sql
├── tests/
├── .env
├── requirements.txt
├── README.md
└── run.py
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/chat_project.git
   cd chat_project
   ```

2. **Install Python packages**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL DB**
   - Create the schema using `database/schema.sql`
   - Add test data if needed with `seed.sql`

4. **Run the server**
   ```bash
   python run.py
   ```

5. **Open `client/index.html` in your browser**  
   (Or serve it through Flask if integrating frontend in backend)

---

## 🛡️ Security Measures

- SQL Injection prevention (parameterized queries)
- XSS protection (user input is sanitized)
- Password storage (to be encrypted)
- Access control for admin features

---

## 👤 Author

**Eyal Raifler**  
11th Grade | De-Shalit High School, Rehovot, Israel 
Cyber Security Final Project – 2025

---

## 📚 License

This project is for educational purposes only.
