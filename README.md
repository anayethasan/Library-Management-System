#  Library Management System API

A RESTful backend API for managing books, authors, members, and borrowing activities in a library.

---

##  Project Info

| | |
|---|---|
| **Version** | v1 |
| **Spec** | OAS 2.0 |
| **Base URL** | `http://127.0.0.1:8000/api` |
| **Swagger UI** | [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) |
| **ReDoc** | [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) |
| **License** | BSD License |
| **Contact** | [contact@phimart.com](mailto:contact@phimart.com) |
| **Terms** | [Terms of Service](https://www.google.com/policies/terms/) |

---

##  Getting Started

### Prerequisites

- Python 3.12+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/library-management-system.git
cd library-management-system

# Create and activate virtual environment
python -m venv .lib-env
.lib-env\Scripts\activate       # Windows
source .lib-env/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (Librarian)
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata library_fixtures.json

# Start the server
python manage.py runserver
```

---

##  Authentication

This API uses **JWT (JSON Web Token)** authentication via `djoser` and `simplejwt`.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/users/` | Register a new user |
| `POST` | `/api/auth/jwt/create/` | Login — get access & refresh token |
| `POST` | `/api/auth/jwt/refresh/` | Refresh access token |
| `POST` | `/api/auth/jwt/verify/` | Verify token |
| `POST` | `/api/auth/logout/` | Logout — blacklist refresh token |

### Usage

```http
Authorization: JWT <your_access_token>
```

---

##  Roles

| Role | Description |
|------|-------------|
| **Librarian** | Admin/Staff user — full access to all resources |
| **Member** | Authenticated user — can view books, borrow and return books |

---

##  API Endpoints

### Authors `/api/authors/`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/authors/` | List all authors | Public |
| `POST` | `/authors/` | Add a new author | Librarian |
| `GET` | `/authors/{id}/` | Get author details | Public |
| `PUT` | `/authors/{id}/` | Update author | Librarian |
| `PATCH` | `/authors/{id}/` | Partial update author | Librarian |
| `DELETE` | `/authors/{id}/` | Delete author | Librarian |

---

### Books `/api/books/`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/books/` | List all books | Public |
| `POST` | `/books/` | Add a new book | Librarian |
| `GET` | `/books/{id}/` | Get book details | Public |
| `PUT` | `/books/{id}/` | Update book | Librarian |
| `PATCH` | `/books/{id}/` | Partial update book | Librarian |
| `DELETE` | `/books/{id}/` | Delete book | Librarian |
| `GET` | `/books/?search=` | Search by title, category, author | Public |
| `GET` | `/books/?category=` | Filter by category | Public |
| `GET` | `/books/?available=true` | Filter available books | Public |

#### Nested — Book Author

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/books/{book_pk}/author/` | Get the author of a specific book | Public |
| `GET` | `/books/{book_pk}/author/{id}/` | Get author detail for a book | Public |

#### Nested — Book Images

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/books/{book_pk}/images/` | List images of a book | Public |
| `POST` | `/books/{book_pk}/images/` | Upload image for a book | Librarian |
| `GET` | `/books/{book_pk}/images/{id}/` | Get specific image | Public |
| `PUT` | `/books/{book_pk}/images/{id}/` | Update image | Librarian |
| `PATCH` | `/books/{book_pk}/images/{id}/` | Partial update image | Librarian |
| `DELETE` | `/books/{book_pk}/images/{id}/` | Delete image | Librarian |

---

### Members `/api/members/`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/members/` | List all members | Librarian |
| `POST` | `/members/` | Register as a member | Authenticated |
| `GET` | `/members/{id}/` | Get member details | Member (own) / Librarian |
| `PUT` | `/members/{id}/` | Update member profile | Member (own) / Librarian |
| `PATCH` | `/members/{id}/` | Partial update member | Member (own) / Librarian |
| `DELETE` | `/members/{id}/` | Delete member | Librarian |

---

### Borrow `/api/borrow/`

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/borrow/` | List borrow records | Member (own) / Librarian (all) |
| `POST` | `/borrow/` | Borrow a book | Member |
| `GET` | `/borrow/{id}/` | Get specific borrow record | Member (own) / Librarian |
| `POST` | `/borrow/{id}/return/` | Return a borrowed book | Member (own) / Librarian |
| `DELETE` | `/borrow/{id}/` | Delete borrow record | Librarian |

#### Borrow a Book — Request Body

```json
{
    "book": 1,
    "due_date": "2026-05-15"
}
```

#### Return a Book — Response

```json
{
    "message": "\"1984\" returned successfully.",
    "late_fee_charged": 40
}
```

>  **Late Fee:** 20 BDT per day after due date.

---

### Dashboard `/api/dashboard/` — Librarian Only

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dashboard/total-books/` | Total books count + full book list |
| `GET` | `/dashboard/total-members/` | Total members count + member list |
| `GET` | `/dashboard/borrowed-books/` | Currently borrowed count + overdue info + list |
| `GET` | `/dashboard/available-books/` | Available books count + list |

#### Sample Response — `/dashboard/borrowed-books/`

```json
{
    "currently_borrowed": 5,
    "overdue_count": 2,
    "borrowed_list": [...]
}
```

---

##  Models

### User (Custom)
| Field | Type |
|-------|------|
| `email` | EmailField (unique, used as username) |
| `address` | TextField |
| `phone_number` | CharField |

### Author
| Field | Type |
|-------|------|
| `name` | CharField |
| `biography` | TextField |
| `created_at` | DateTimeField |

### Book
| Field | Type |
|-------|------|
| `title` | CharField |
| `isbn` | CharField (unique) |
| `category` | CharField (choices) |
| `available` | BooleanField |
| `author` | ForeignKey → Author |
| `created_at` | DateTimeField |

### BookImage
| Field | Type |
|-------|------|
| `book` | ForeignKey → Book |
| `image` | CloudinaryField |

### Member
| Field | Type |
|-------|------|
| `user` | OneToOneField → User |
| `membership_date` | DateField |
| `created_at` | DateTimeField |

### BorrowRecord
| Field | Type |
|-------|------|
| `book` | ForeignKey → Book |
| `member` | ForeignKey → Member |
| `borrow_date` | DateTimeField |
| `due_date` | DateField |
| `return_date` | DateTimeField (nullable) |
| `status` | CharField (`borrowed` / `returned`) |
| `late_fee_charged` | PositiveIntegerField |

---

##  Relationships

```
User ──(OneToOne)──► Member
                        │
                        └──(FK)──► BorrowRecord ◄──(FK)── Book
                                                              │
Author ──(FK)──────────────────────────────────────────────► Book
                                                              │
                                                         BookImage
```

---

##  Project Structure

```
library_management/         # Main config
├── settings.py
├── urls.py
└── views.py                # Root view

api/                        # API routing
├── urls.py
└── permissions.py

users/                      # Custom user
├── models.py
├── manager.py
├── admin.py
└── urls.py

member/                     # Member app
├── models.py
├── serializers.py
└── views.py

books/                      # Books & Authors
├── models.py
├── serializers.py
├── views.py
├── filters.py
├── pagination.py
└── validators.py

borrow/                     # Borrow logic
├── models.py
├── serializers.py
├── views.py
├── services.py
└── dashboard.py
```

---

##  Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

---

##  Tech Stack

| | |
|---|---|
| **Framework** | Django 5.x + Django REST Framework |
| **Auth** | Djoser + SimpleJWT |
| **Image Storage** | Cloudinary |
| **Filtering** | django-filter |
| **Nested Routes** | drf-nested-routers |
| **API Docs** | drf-yasg (Swagger / ReDoc) |
| **Debug** | django-debug-toolbar |
| **Database** | SQLite (dev) |

##  License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Anayet Hasan Niloy**
Software Engineer | CSE Student at ISTT | Competitive Programmer

> Built with  using Django REST Framework