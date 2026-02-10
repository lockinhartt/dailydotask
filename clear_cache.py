import os
import shutil

# Clear Python cache
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        pycache_path = os.path.join(root, '__pycache__')
        print(f'Removing {pycache_path}')
        shutil.rmtree(pycache_path)
    
    # Remove .pyc files
    for file in files:
        if file.endswith('.pyc'):
            file_path = os.path.join(root, file)
            print(f'Removing {file_path}')
            os.remove(file_path)

print("✅ Cache cleared! Please restart your server.")
print("Press Ctrl+C in your terminal running the server, then run: python manage.py runserver")
