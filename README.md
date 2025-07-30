# EMR-Patient-Registration-System-Backend

This is the backend for the **Multi-Facility EMR Patient Registration System**, developed using Django and PostgreSQL. The system allows for secure patient registration across multiple healthcare facilities and services like labs and radiology.

---

## 🌟 Features

- 🏥 Multi-Facility Support
- 🧍 Patient Registration with MRN (Medical Record Number)
- 🔍 Search by name or MRN
- 🔐 OAuth2 Token Authentication via `django-oauth-toolkit`
- 🗃️ PostgreSQL Database
- ⚙️ CRUD APIs for Patients, Facilities, Services
- 📄 Paginated & JSON responses
- 🔁 CSRF-Protected Endpoints

---

## 🛠 Tech Stack

- **Backend Framework**: Django 5.2
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: OAuth2 via `django-oauth-toolkit`
- **Pagination**: DRF's `PageNumberPagination`
- **Environment Configuration**: `python-decouple`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:Bwire2010/EMR-Patient-Registration-System-Backend.git
cd emr-backend
```

---

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv myenv
source myenv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set Up `.env` File

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=kojo
DB_USER=neeraj
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

> Replace values with your actual database settings

---

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

### 7. Run the Server

```bash
python manage.py runserver
```

> Server will start at: `http://127.0.0.1:8000/`

---

## 🔑 Authentication (OAuth2)

### Token Request Endpoint

```http
POST /api/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Response:

```json
{
  "access_token": "your_token_here",
  "expires_in": 3600,
  "token_type": "Bearer",
  "scope": "read write"
}
```

### Use the Token:

```http
Authorization: Bearer your_token_here
```

---

## 🔍 API Endpoints

| Method | Endpoint                    | Description                  |
|--------|-----------------------------|------------------------------|
| GET    | `/api/patients/`            | List patients                |
| POST   | `/api/patients/`            | Create a patient             |
| GET    | `/api/patients/search/?q=`  | Search by name or MRN        |
| PATCH  | `/api/patients/{id}/`       | Update a patient             |
| DELETE | `/api/patients/{id}/`       | Delete a patient             |
| GET    | `/api/facilities/`          | List facilities              |
| GET    | `/api/services/`            | List service types           |

---

## 🧱 Project Structure

```
emr_system/
├── emr_core/
│   ├── settings.py
│   └── urls.py
├── patients/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
├── manage.py
├── requirements.txt
├── .env
```

---

## 🔐 Security

- Authentication via OAuth2 password grant
- Uses Django’s built-in CSRF middleware
- Protected views require Bearer tokens
- Production WSGI/ASGI recommended for deployment

---

## 📦 requirements.txt Example

> If you don't have it yet, here's a basic one:

```txt
Django>=5.2,<6.0
djangorestframework
django-oauth-toolkit
python-decouple
psycopg2-binary
django-cors-headers
```

---


## 🧠 License

MIT License

---

## ✍️ Author

Patrobas Bwire – [LinkedIn](https://www.linkedin.com/in/your-profile)
