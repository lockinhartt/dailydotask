# ULTIMATE FIX: Delete Django's bytecode cache and restart clean
import os
import shutil
import subprocess
import time

print("🔥 ULTIMATE CACHE DESTROYER 🔥")
print("=" * 50)

# Stop any running servers (this script assumes it's run separately)
# Clear ALL Python cache
cache_dirs = []
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_path = os.path.join(root, '__pycache__')
        cache_dirs.append(cache_path)
        
print(f"Found {len(cache_dirs)} cache directories")

for cache_dir in cache_dirs:
    try:
        shutil.rmtree(cache_dir)
        print(f"✅ Deleted: {cache_dir}")
    except Exception as e:
        print(f"❌ Failed to delete {cache_dir}: {e}")

# Delete .pyc files
pyc_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pyc'):
            pyc_path = os.path.join(root, file)
            pyc_files.append(pyc_path)

print(f"\nFound {len(pyc_files)} .pyc files")
for pyc_file in pyc_files:
    try:
        os.remove(pyc_file)
        print(f"✅ Deleted: {pyc_file}")
    except Exception as e:
        print(f"❌ Failed to delete {pyc_file}: {e}")

print("\n" + "=" * 50)
print("✅ CACHE DESTRUCTION COMPLETE!")
print("=" * 50)
print("\nNow run: python manage.py runserver")
