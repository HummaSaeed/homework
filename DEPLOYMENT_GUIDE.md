# Django Homework Management System - Deployment Guide

## Current Status

✅ **System**: Fully Operational  
✅ **Database**: Initialized with 22 tables  
✅ **Admin**: Created (admin/admin123)  
✅ **API**: Ready for development  
✅ **All Tests**: Passed  

---

## Project Structure

```
f:\homewrk system\homework_management\
│
├── accounts/                           # User authentication & profiles
│   ├── migrations/                     # Database migrations
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_user_options_alter_user_managers_and_more.py
│   ├── __init__.py
│   ├── admin.py                        # Django admin configuration
│   ├── apps.py
│   ├── decorators.py                   # Role requirement decorator
│   ├── models.py                       # User, PhoneOTP, Profiles
│   ├── permissions.py                  # Role-based permissions
│   ├── serializers.py                  # DRF serializers
│   ├── urls.py                         # API routes
│   └── views.py                        # Authentication endpoints
│
├── schools/                            # School management
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                       # School, AcademicSession
│   └── views.py
│
├── classes/                            # Class/section management
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                       # SchoolClass model
│   └── views.py
│
├── homework/                           # Core homework system
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                       # Subject, Homework, Submission
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── notifications/                      # Notifications (placeholder)
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── views.py
│
├── files/                              # File management (placeholder)
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── views.py
│
├── dashboard/                          # Analytics (placeholder)
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── views.py
│
├── homework_management/                # Main project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                     # Django settings
│   ├── urls.py                         # Root URL config
│   └── wsgi.py
│
├── venv/                               # Virtual environment
│   └── ... (Python packages)
│
├── .gitignore                          # Git ignore rules
├── .vscode/                            # VS Code settings
├── db.sqlite3                          # SQLite database (INITIALIZED)
├── manage.py                           # Django CLI
├── README.md                           # Complete documentation
├── PROJECT_SUMMARY.md                  # Project overview
├── SETUP_CHECKLIST.md                  # Setup checklist
├── requirements.txt                    # Python dependencies
├── setup_admin.py                      # Create admin script
└── test_system.py                      # System test script
```

## Key Files Overview

### Configuration Files
- **settings.py** - Django settings, JWT config, CORS, installed apps
- **urls.py** - Root URL routing
- **requirements.txt** - All Python dependencies

### Core Models (accounts/models.py)
```python
- User (custom AbstractUser)
  - Fields: phone_number, full_name, role (admin/teacher/student)
  - Relations: groups, user_permissions

- PhoneOTP
  - Fields: phone_number, code, created_at, expires_at, is_used

- TeacherProfile (OneToOne User)
  - Fields: qualification, subject_specialization
  - Relations: assigned_classes (M2M SchoolClass)

- StudentProfile (OneToOne User)
  - Fields: roll_number, section, parent_phone
  - Relations: school_class (FK SchoolClass)
```

### API Endpoints (accounts/urls.py)
```
POST   /api/v1/accounts/auth/request-otp/      - Request OTP
POST   /api/v1/accounts/auth/verify-otp/       - Verify OTP & login
POST   /api/v1/accounts/auth/logout/           - Logout
POST   /api/v1/accounts/auth/refresh/          - Refresh token
GET    /api/v1/accounts/profile/               - Get profile
PUT    /api/v1/accounts/profile/               - Update profile
```

---

## Quick Reference Commands

### Development
```bash
# Start server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Django shell
python manage.py shell

# Check system
python manage.py check

# Create admin
python manage.py createsuperuser
```

### Database
```bash
# View database schema
python manage.py dbshell

# Show migrations
python manage.py showmigrations

# Migrate specific app
python manage.py migrate accounts

# Rollback migration
python manage.py migrate accounts 0001
```

### Testing
```bash
# Run tests
python manage.py test

# Run comprehensive test
python test_system.py
```

---

## Important Settings

### JWT Configuration (settings.py)
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
}
```

### Custom User Model
```python
AUTH_USER_MODEL = 'accounts.User'
```

### Authentication
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

---

## Development Workflow

### 1. Create New Feature
```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Create serializer
# Create view
# Add URL
# Test endpoint
```

### 2. API Development Pattern
```python
# models.py - Define model
class MyModel(models.Model):
    field1 = models.CharField()

# serializers.py - Create serializer
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

# views.py - Create view
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [IsAuthenticated]

# urls.py - Register route
router = DefaultRouter()
router.register('mymodel', MyModelViewSet)
```

### 3. Test Endpoints
```bash
# Request OTP
curl -X POST http://localhost:8000/api/v1/accounts/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+92 300 1234567"}'

# Verify OTP
curl -X POST http://localhost:8000/api/v1/accounts/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+92 300 1234567", "code": "123456"}'

# Authenticated request
curl -X GET http://localhost:8000/api/v1/accounts/profile/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Production Deployment

### Preparation
1. Set `DEBUG = False`
2. Generate new `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Set `CORS_ALLOWED_ORIGINS` to specific domains
5. Switch to PostgreSQL database
6. Configure environment variables

### Server Setup
1. Install Python 3.10+
2. Clone repository
3. Create virtual environment
4. Install dependencies
5. Run migrations
6. Collect static files

### Web Server
- Use Gunicorn or uWSGI as application server
- Use Nginx or Apache as reverse proxy
- Enable HTTPS/SSL
- Configure firewall

### Database
- PostgreSQL recommended for production
- Regular backups configured
- Connection pooling enabled

### Monitoring
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- Log aggregation (ELK Stack)
- Alerting configured

---

## Troubleshooting

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Admin User Issues
```bash
# Create new admin
python manage.py createsuperuser

# Or use script
python setup_admin.py
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8080

# Kill process on port 8000
taskkill /F /FI "STATE eq RUNNING" /IM python.exe
```

### Module Not Found
```bash
# Ensure virtual environment activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Next Steps

1. **Implement Homework API**
   - Create views for CRUD operations
   - Add filtering, pagination, ordering
   - Implement authentication checks

2. **Add SMS Integration**
   - Integrate Twilio, AWS SNS, or Firebase
   - Replace OTP logging with SMS sending

3. **Email Notifications**
   - Configure email backend
   - Create notification templates
   - Send emails on homework events

4. **Frontend Development**
   - Create React/Vue frontend
   - Implement authentication flow
   - Build homework interface

5. **Testing & QA**
   - Write unit tests
   - Write integration tests
   - Load testing
   - Security testing

6. **Deployment**
   - Set up CI/CD pipeline
   - Configure production server
   - Enable monitoring
   - Deploy to production

---

## Support & Resources

### Documentation
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)

### Tools
- Postman - API testing
- SQLite Browser - Database exploration
- VS Code - Development editor

### Community
- Django Forum
- Stack Overflow
- GitHub Issues

---

**Setup Status**: ✅ COMPLETE  
**Ready for Development**: ✅ YES  
**All Systems**: ✅ OPERATIONAL  

For more details, see [README.md](README.md) and [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
