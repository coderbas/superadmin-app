# SuperAdminApp

A full‐stack “SuperAdmin” interface built with Django REST Framework (backend) and React + Bootstrap (frontend).  
Admins can create and manage users (granting/revoking superuser status) and assign page‐level permissions. All authenticated users can view a Products List and post comments.

---

## 📦 Deliverables

A single parent directory containing:

- `frontend/` → React application  
- `backend/` → Django REST API  
- `requirements.txt` in `backend/` for Python dependencies  
- `package.json` in `frontend/` for Node dependencies  
- A top‐level `README.md` (this file) explaining:
  1. Setup instructions (both backend and frontend)  
  2. Features breakdown  
  3. Folder structure overview  
  4. Challenges faced & solutions  
  5. How to zip or push to GitHub  

---

## 🚀 Setup Instructions

### 1. Clone the repository (or unzip the delivered folder)
```bash
git clone https://github.com/your‐username/superadmin‐app.git
cd superadmin‐app

2. Backend (Django REST API)
  1. Create & activate a virtual environment (recommended):
      cd backend
      python3 -m venv venv
      # On Windows:
      venv\Scripts\activate
      # On macOS/Linux:
      source venv/bin/activate
  2. Install Python dependencies:
       
        pip install --upgrade pip
        pip install -r requirements.txt
  3. Apply database migrations:
        python manage.py migrate

  4.  Create a superuser (to log into Django Admin & test admin routes):    
        python manage.py createsuperuser

        Follow prompts to set username, email, and password.


  5.  Run the Django development server:
        python manage.py runserver

        By default, the API is available at http://127.0.0.1:8000/api/ and the Django Admin at http://127.0.0.1:8000/admin/.

