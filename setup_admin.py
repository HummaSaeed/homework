#!/usr/bin/env python
"""Create default admin user"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_management.settings')
django.setup()

from accounts.models import User

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@homework.local',
        password='admin123',
        phone_number='1234567890',
        full_name='Admin User',
        role='admin'
    )
    print("✓ Superuser 'admin' created successfully")
else:
    print("✓ Superuser 'admin' already exists")

# Verify database
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n✓ Database has {len(tables)} tables:")
    for table in sorted(tables):
        print(f"  - {table[0]}")
