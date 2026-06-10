# Django Homework Management System

A comprehensive Django REST API for managing homework assignments, tracking submissions, and grading across schools with role-based access control (Admin, Teacher, Student).

## Features

- **User Authentication**: OTP-based phone authentication with JWT tokens
- **Role-Based Access Control**: Admin, Teacher, and Student roles with permission management
- **Homework Management**: Create, assign, and grade homework assignments
- **Submission Tracking**: Track student submissions with file uploads and feedback
- **School & Class Management**: Manage schools, academic sessions, and classes
- **Teacher & Student Profiles**: Specialized profiles for different user types
- **Subject Management**: Organize homework by subjects
- **File Upload Support**: Handle homework attachments and student submissions
- **Notifications System**: Notify users of assignments and grades (foundation ready)
- **Django Admin**: Full admin interface for content management

## Technology Stack

- **Framework**: Django 4.2.0
- **API**: Django REST Framework 3.14.0
- **Authentication**: JWT via djangorestframework-simplejwt 5.2.2
- **Database**: SQLite3 (development) / PostgreSQL (production-ready)
- **CORS**: django-cors-headers 3.14.0
- **Filtering**: django-filter 23.1
- **Image Processing**: Pillow 9.5.0

## Project Structure

```
homework_management/
├── accounts/                    # User authentication and profiles
│   ├── models.py               # User, PhoneOTP, TeacherProfile, StudentProfile
│   ├── views.py                # OTP, JWT authentication endpoints
│   ├── serializers.py          # User and profile serializers
│   ├── permissions.py          # Role-based permission classes
│   ├── decorators.py           # Role requirement decorators
│   ├── urls.py                 # Auth API routes
│   ├── admin.py                # Django admin configuration
│   ├── migrations/             # Database migrations
│   └── __init__.py
├── schools/                     # School and academic management
│   ├── models.py               # School, AcademicSession
│   ├── admin.py                # Admin configuration
│   ├── migrations/
│   └── __init__.py
├── classes/                     # Class and section management
│   ├── models.py               # SchoolClass
│   ├── admin.py                # Admin configuration
│   ├── migrations/
│   └── __init__.py
├── homework/                    # Core homework system
│   ├── models.py               # Subject, Homework, Submission
│   ├── views.py                # Homework API endpoints
│   ├── serializers.py          # Homework serializers
│   ├── admin.py                # Admin configuration
│   ├── migrations/             # Database migrations
│   ├── urls.py                 # Homework API routes
│   └── __init__.py
├── notifications/               # Notification system (foundation)
│   ├── models.py
│   ├── admin.py
│   └── __init__.py
├── files/                       # File management (foundation)
│   ├── models.py
│   ├── admin.py
│   └── __init__.py
├── dashboard/                   # Analytics dashboard (foundation)
│   ├── models.py
│   ├── admin.py
│   └── __init__.py
├── homework_management/         # Main project configuration
│   ├── settings.py             # Django settings, JWT config, CORS
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py                 # WSGI configuration
│   ├── asgi.py                 # ASGI configuration
│   └── __init__.py
├── manage.py                   # Django CLI management script
├── db.sqlite3                  # Development database
├── requirements.txt            # Python dependencies
├── setup_admin.py              # Script to create admin user
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
└── venv/                       # Python virtual environment
```

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Windows/Mac/Linux OS

### 1. Navigate to Project Directory
```bash
cd "f:\homewrk system\homework_management"
```

### 2. Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Create Admin User

**Option A: Using Django admin creation:**
```bash
python manage.py createsuperuser
```

**Option B: Using setup script:**
```bash
python setup_admin.py
```

This creates:
- Username: `admin`
- Password: `admin123`
- Email: `admin@homework.local`
- Role: Admin

### 6. Start Development Server
```bash
python manage.py runserver
```

The server will be available at: `http://localhost:8000`

## API Endpoints

### Authentication Endpoints (`/api/v1/accounts/`)

**Request OTP**
```
POST /api/v1/accounts/auth/request-otp/
Content-Type: application/json

{
  "phone_number": "+92 300 1234567"
}

Response:
{
  "message": "OTP sent to your phone",
  "phone_number": "+92 300 1234567"
}
```

**Verify OTP & Get Tokens**
```
POST /api/v1/accounts/auth/verify-otp/
Content-Type: application/json

{
  "phone_number": "+92 300 1234567",
  "code": "123456"
}

Response:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "user_phone",
    "full_name": "User Name",
    "phone_number": "+92 300 1234567",
    "email": "user@example.com",
    "role": "student"
  }
}
```

**Get User Profile**
```
GET /api/v1/accounts/profile/
Authorization: Bearer <access_token>

Response:
{
  "id": 1,
  "username": "user_phone",
  "full_name": "User Name",
  "phone_number": "+92 300 1234567",
  "email": "user@example.com",
  "role": "student",
  "profile_image": null,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Update Profile**
```
PUT /api/v1/accounts/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "Updated Name",
  "email": "newemail@example.com"
}
```

**Logout**
```
POST /api/v1/accounts/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

**Refresh Token**
```
POST /api/v1/accounts/auth/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}

Response:
{
  "access": "new_access_token"
}
```

## Authentication Flow

### OTP-Based Authentication

1. User submits phone number to `/auth/request-otp/`
2. System generates 6-digit OTP (expires in 5 minutes)
3. OTP is stored in database (TODO: integrate SMS gateway for delivery)
4. User submits OTP to `/auth/verify-otp/`
5. System verifies OTP and returns JWT tokens
6. Client includes access token in all future requests:
   ```
   Authorization: Bearer <access_token>
   ```

### Token Configuration

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled (new refresh token on each use)
- **Blacklist on Rotation**: Enabled (old tokens invalidated)
- **Algorithm**: HS256

## Database Schema

### User Management
- **User**: Custom user model extending AbstractUser
  - Fields: username, email, phone_number, full_name, role, profile_image, is_active
  - Roles: admin, teacher, student
  - Related: groups, user_permissions

- **PhoneOTP**: OTP authentication tokens
  - Fields: phone_number, code (6-digit), created_at, expires_at (5 min), is_used

- **TeacherProfile**: Teacher-specific information
  - Fields: user (OneToOne), qualification, subject_specialization
  - Relations: assigned_classes (M2M to SchoolClass)

- **StudentProfile**: Student-specific information
  - Fields: user (OneToOne), roll_number, section, parent_phone
  - Relations: school_class (FK to SchoolClass)

### Academic Structure
- **School**: School information
  - Fields: name, logo, address, phone, principal_name

- **AcademicSession**: School semesters/years
  - Fields: school (FK), name, start_date, end_date, is_active

- **SchoolClass**: Classes with sections
  - Fields: class_name, section, class_teacher (FK), school (FK)
  - Unique constraint: (class_name, section, school)

### Homework System
- **Subject**: Course subjects
  - Fields: name, code (unique), description

- **Homework**: Assignments
  - Fields: title, description, subject (FK), assigned_by (FK), assigned_to (M2M)
  - Fields: due_date, status (draft/assigned/completed/graded), points
  - Fields: attachments (FileField)

- **Submission**: Student work
  - Fields: homework (FK), student (FK), submission_file (FileField)
  - Fields: status (submitted/graded), score, feedback, graded_by (FK)
  - Unique constraint: (homework, student)

### Total Tables: 22
- Core: 5 (User, PhoneOTP, TeacherProfile, StudentProfile, others)
- Academic: 3 (School, AcademicSession, SchoolClass)
- Homework: 4 (Subject, Homework, Submission, Homework_assigned_to)
- Django system: 10 (auth, admin, contenttypes, sessions, token_blacklist, etc.)

## Django Admin

Access admin panel at: `http://localhost:8000/admin/`

**Features:**
- User and profile management
- School and class administration
- Homework creation and grading
- OTP management and monitoring
- Academic session management

## User Roles & Permissions

### Admin
- Full system access
- Manage users, schools, classes
- View all homework and submissions
- System configuration

### Teacher
- Create and assign homework
- Grade submissions
- View assigned classes
- Access their students' work

### Student
- View assigned homework
- Submit homework
- View grades and feedback
- Update profile

## Configuration

### Key Settings (settings.py)
```python
# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ Change in production

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## Development Commands

### Check Configuration
```bash
python manage.py check
```

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Reset Database
```bash
rm db.sqlite3  # or: del db.sqlite3 on Windows
python manage.py migrate
python manage.py createsuperuser
```

### Database Shell
```bash
python manage.py dbshell
```

### Run Django Shell
```bash
python manage.py shell
```

### List All URLs
```bash
python manage.py show_urls
```

### Run Tests
```bash
python manage.py test
```

### Collect Static Files
```bash
python manage.py collectstatic
```

## Testing the API

### Using cURL

**Request OTP:**
```bash
curl -X POST http://localhost:8000/api/v1/accounts/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+92 300 1234567"}'
```

**Verify OTP:**
```bash
curl -X POST http://localhost:8000/api/v1/accounts/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+92 300 1234567", "code": "123456"}'
```

**Get Profile:**
```bash
curl -X GET http://localhost:8000/api/v1/accounts/profile/ \
  -H "Authorization: Bearer <access_token>"
```

### Using Postman

1. Import API endpoints into Postman
2. Set base URL: `http://localhost:8000/api/v1`
3. For authenticated requests, add header:
   ```
   Authorization: Bearer <access_token>
   ```

## Database Reset & Recovery

### Full Reset
```bash
# Stop the server first
python manage.py migrate --fake-initial
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Specific App Reset
```bash
python manage.py migrate accounts zero
python manage.py migrate accounts
```

## Deployment Checklist

- [ ] Change `DEBUG = False` in settings.py
- [ ] Update `SECRET_KEY` to a secure value
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up environment variables for sensitive data
- [ ] Configure PostgreSQL or production database
- [ ] Set up proper file storage (AWS S3, etc.)
- [ ] Configure HTTPS/SSL
- [ ] Set `CORS_ALLOW_ALL_ORIGINS = False` and specify allowed domains
- [ ] Configure proper logging
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Run `python manage.py collectstatic`
- [ ] Use production WSGI server (Gunicorn, uWSGI, etc.)
- [ ] Set up load balancer and reverse proxy (Nginx, etc.)

## Known Limitations & TODO

- [ ] **OTP SMS Integration**: Currently logs OTP to console (TODO: integrate Twilio, AWS SNS, or similar)
- [ ] **Rate Limiting**: Configured in requirements but not yet applied to views
- [ ] **Email Notifications**: Not yet implemented
- [ ] **Dashboard Analytics**: Foundation ready, implementation pending
- [ ] **WebSocket Support**: For real-time notifications
- [ ] **File Storage**: No external storage configured (local filesystem only)
- [ ] **Production Database**: PostgreSQL setup guide needed
- [ ] **API Documentation**: Swagger/OpenAPI documentation
- [ ] **Automated Tests**: Test suite needs expansion
- [ ] **Mobile App**: React Native or Flutter integration

## Troubleshooting

### "No module named 'accounts'"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Verify INSTALLED_APPS in settings.py
python manage.py check
```

### "ModuleNotFoundError: No module named 'PIL'"
```bash
pip install Pillow
```

### Database migration errors
```bash
# Remove corrupted database
rm db.sqlite3  # or: del db.sqlite3 on Windows

# Reapply migrations
python manage.py migrate
```

### CORS errors when accessing from frontend
```python
# Update settings.py:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React app
    "http://localhost:3001",
    "https://yourdomain.com",
]
```

### Port 8000 already in use
```bash
# Use different port
python manage.py runserver 8080

# Or find and kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti :8000 | xargs kill -9
```

## Performance Optimization

### Database
- Add indexing for frequently queried fields
- Use `select_related()` and `prefetch_related()` in views
- Implement caching (Redis recommended)

### API
- Add pagination for list endpoints
- Implement request throttling
- Use compression (gzip)
- Optimize image uploads

### Static Files
- Use CDN for static assets
- Enable gzip compression
- Set proper cache headers

## Architecture Decisions

1. **Custom User Model**: Extended AbstractUser for flexibility in adding custom fields (phone_number, role, etc.)

2. **OTP Authentication**: Chose OTP over traditional password auth for better UX and security in educational context

3. **JWT Tokens**: Selected djangorestframework-simplejwt for modern token-based authentication

4. **Multi-App Structure**: Separated concerns into distinct apps (accounts, schools, classes, homework) for maintainability

5. **Role-Based Permissions**: Three roles (admin/teacher/student) for granular access control

6. **SQLite (Dev) / PostgreSQL (Prod)**: SQLite for development simplicity, PostgreSQL recommended for production due to better concurrency

## Dependencies Explanation

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.0 | Web framework |
| djangorestframework | 3.14.0 | REST API development |
| djangorestframework-simplejwt | 5.2.2 | JWT authentication |
| django-cors-headers | 3.14.0 | CORS handling |
| django-filter | 23.1 | API filtering |
| django-ratelimit | 3.0.1 | Rate limiting (TODO) |
| Pillow | 9.5.0 | Image processing |
| python-decouple | 3.8 | Environment config |

## Community & Support

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Issue Tracker**: GitHub Issues
- **Documentation**: See README.md and SKILL.md files

## License

This project is created for educational purposes.

---

**Project Status**: ✅ Complete - All migrations applied, database initialized, admin created  
**Database**: 22 tables created and operational  
**API**: Authentication endpoints ready for use  
**Version**: 2.0.0  
**Last Updated**: January 2025  

## Quick Start Summary

```bash
# 1. Activate environment
.\venv\Scripts\Activate.ps1  # Windows

# 2. Apply migrations
python manage.py migrate

# 3. Create admin
python manage.py createsuperuser

# 4. Start server
python manage.py runserver

# 5. Access
# Admin: http://localhost:8000/admin
# API: http://localhost:8000/api/v1/accounts/
```

---

For detailed setup and development information, refer to this README.

- [ ] **OTP SMS Integration**: Currently logs OTP to console (TODO: integrate Twilio, AWS SNS, or similar)
- [ ] **Rate Limiting**: Configured in requirements but not yet applied to views
- [ ] **Email Notifications**: Not yet implemented
- [ ] **Dashboard Analytics**: Foundation ready, implementation pending
- [ ] **WebSocket Support**: For real-time notifications
- [ ] **File Storage**: No external storage configured (local filesystem only)
- [ ] **Production Database**: PostgreSQL setup guide needed
- [ ] **API Documentation**: Swagger/OpenAPI documentation
- [ ] **Automated Tests**: Test suite needs expansion
- [ ] **Mobile App**: React Native or Flutter integration

## Troubleshooting

### "No module named 'accounts'"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Verify INSTALLED_APPS in settings.py
python manage.py check
```

### "ModuleNotFoundError: No module named 'PIL'"
```bash
pip install Pillow
```

### Database migration errors
```bash
# Remove corrupted database
rm db.sqlite3  # or: del db.sqlite3 on Windows

# Reapply migrations
python manage.py migrate
```

### CORS errors when accessing from frontend
```python
# Update settings.py:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React app
    "http://localhost:3001",
    "https://yourdomain.com",
]
```

### Port 8000 already in use
```bash
# Use different port
python manage.py runserver 8080

# Or find and kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti :8000 | xargs kill -9
```

## Performance Optimization

### Database
- Add indexing for frequently queried fields
- Use `select_related()` and `prefetch_related()` in views
- Implement caching (Redis recommended)

### API
- Add pagination for list endpoints
- Implement request throttling
- Use compression (gzip)
- Optimize image uploads

### Static Files
- Use CDN for static assets
- Enable gzip compression
- Set proper cache headers

## Architecture Decisions

1. **Custom User Model**: Extended AbstractUser for flexibility in adding custom fields (phone_number, role, etc.)

2. **OTP Authentication**: Chose OTP over traditional password auth for better UX and security in educational context

3. **JWT Tokens**: Selected djangorestframework-simplejwt for modern token-based authentication

4. **Multi-App Structure**: Separated concerns into distinct apps (accounts, schools, classes, homework) for maintainability

5. **Role-Based Permissions**: Three roles (admin/teacher/student) for granular access control

6. **SQLite (Dev) / PostgreSQL (Prod)**: SQLite for development simplicity, PostgreSQL recommended for production due to better concurrency

## Dependencies Explanation

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.0 | Web framework |
| djangorestframework | 3.14.0 | REST API development |
| djangorestframework-simplejwt | 5.2.2 | JWT authentication |
| django-cors-headers | 3.14.0 | CORS handling |
| django-filter | 23.1 | API filtering |
| django-ratelimit | 3.0.1 | Rate limiting (TODO) |
| Pillow | 9.5.0 | Image processing |
| python-decouple | 3.8 | Environment config |

## Community & Support

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Issue Tracker**: GitHub Issues
- **Documentation**: See README.md and SKILL.md files

## License

This project is created for educational purposes.

---

**Project Status**: ✅ Complete - All migrations applied, database initialized, admin created  
**Database**: 22 tables created and operational  
**API**: Authentication endpoints ready for use  
**Version**: 2.0.0  
**Last Updated**: January 2025
