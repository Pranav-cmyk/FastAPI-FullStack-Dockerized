# Full-Stack Containerized Task Management API

A robust, full-stack Todo application built with **FastAPI**, **SQLAlchemy**, and **Jinja2 Templates**. This project demonstrates a production-ready architecture with secure JWT authentication, role-based access control, and a fully containerized deployment lifecycle using Docker.

## 🚀 Features

- **Secure Authentication:** JWT (JSON Web Tokens) based authentication with secure password hashing using bcrypt.
- **Role-Based Access Control (RBAC):** Distinct privileges for regular users and administrators.
- **CRUD Operations:** Complete Create, Read, Update, and Delete functionality for tasks and users.
- **Server-Side Rendering:** Clean and responsive frontend built with Jinja2 templates, HTML5, CSS3, and Bootstrap.
- **Database ORM & Scalability:** SQLAlchemy integration for seamless database interactions and architectural flexibility to switch between **PostgreSQL**, **SQLite**, and **MySQL** with minimal configuration changes.
- **Data Migrations:** Alembic configured for version-controlled schema migrations, ensuring long-term data scalability and consistent database states across different environments.
- **Containerization:** Fully dockerized with `Dockerfile` and `compose.yaml` for consistent development and deployment environments.

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python 3.11+
- **Database:** SQLite (Default for development) / PostgreSQL ready
- **ORM & Migrations:** SQLAlchemy, Alembic
- **Security:** Passlib, python-jose (JWT), bcrypt
- **Frontend:** Jinja2 Templates, HTML, CSS, JavaScript (Bootstrap)
- **DevOps:** Docker, Docker Compose

## 📂 Project Structure

```text
├── alembic/                # Database migration scripts
├── database/               # SQLAlchemy models and database connection
├── routers/                # API route handlers (auth, users, todos, admin)
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # Jinja2 HTML templates
├── utils/                  # Utility functions (auth, hashing, dependencies)
├── main.py                 # FastAPI application entry point
├── Dockerfile              # Docker image configuration
├── compose.yaml            # Docker Compose multi-container orchestration
├── requirements.txt        # Python dependencies
└── pyproject.toml          # Project metadata
```

## ⚙️ Prerequisites

- **Docker** and **Docker Compose** (Recommended)
- **Python 3.11+** (If running locally without Docker)

## 🐳 Running with Docker (Recommended)

The easiest way to get the application running is via Docker Compose.

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd First-Full-Stack-App
   ```

2. **Set up Environment Variables:**
   Ensure you have the required environment variables in your `compose.yaml` or a `.env` file:
   ```env
   SECRET_KEY=your_super_secret_key
   ALGORITHM=HS256
   SQL_ALCHEMY_URL=sqlite:///./sql_app.db
   ```

3. **Build and Run the Containers:**
   ```bash
   docker compose up --build
   ```

4. **Access the Application:**
   Open your browser and navigate to: `http://localhost:8000`

## 💻 Running Locally (Without Docker)

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations (Optional but recommended):**
   ```bash
   alembic upgrade head
   ```

4. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 📖 API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access them at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 👨‍💻 Author

**Pranav Sagar**
- [LinkedIn](https://www.linkedin.com/in/pranav-sagar-fsd?utm_source=share_via&utm_content=profile&utm_medium=member_android)
- Full Stack AI Engineer & Robotics Researcher
