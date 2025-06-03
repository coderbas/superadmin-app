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

3. Frontend (React)
    1.Open a new terminal, then:
              cd ../frontend
    2.Install Node dependencies:
          npm install
      If you encounter peer‐dependency conflicts, try:
          npm install --legacy-peer-deps

    3.Start the React development server:

        npm start
      This will launch the frontend at http://localhost:3000. It proxies API calls to                 http://127.0.0.1:8000/api/.




4. Usage
     1. Register a user (optional):
      
      Visit http://127.0.0.1:8000/admin/ → log in with your Django superuser → create additional User             entries (they are active by default, non‐superuser).
      
      Alternatively, the backend user‐creation endpoint (POST /api/users/) is only available to superusers.
      
    2.  Log in via the React frontend:
      
      Go to http://localhost:3000/login
      
      Use your Django superuser credentials (or any active user)
      
      On successful login, you’ll see the Products List page (all authenticated users) and—if you are a           superuser—the Admin Dashboard and Users page in the navbar.
      
      3. Admin Dashboard (for superusers only):
      
      Accessible from http://localhost:3000/admin
      
      View all users, toggle “Superuser” status, and “Add User” via a modal form.
      
      4. Users Page (superuser-only):
      
      Accessible from http://localhost:3000/pages/users
      
      Displays a live table of all users, their email, active/superuser flags, and allows granting/revoking       superuser.
      
      5. Products List (all logged-in users):
      
      Accessible from http://localhost:3000/pages/products-list
      
      Shows a table of products (fetched from /api/products/).
      
      Underneath, it shows “Comments” for that page (page_id=1) and a form to post new comments.
      
      6. Comments Section:
      
      Endpoint: GET /api/comments/?page_id=1
      
      Posting a comment: POST /api/comments/ with JSON { "page": 1, "content": "Your comment text" } and           Authorization header.
      
      Only authenticated users can view/post comments.

Features Breakdown
         1.  Authentication & JWT
          
          Custom JWT token pair endpoint (/api/token/) adds username and is_superuser into the access token.
          
          Refresh endpoint at /api/token/refresh/.
          
          React AuthContext checks localStorage for access_token, decodes it, then fetches full user data             via /api/accounts/user/<id>/, setting user.is_superuser.
          
          Inactivity timer logs out after 1 hour of no activity (click/keydown/mousemove).
          
          2. Admin Dashboard (React)
          
          Navbar shows “Admin Dashboard” & “Users” links only if user.is_superuser === true.
          
          /admin route protected—redirects non‐superusers to /login.
          
          “User List” table fetches GET /api/users/ (superuser‐only) and displays ID, username, email,                 active, superuser status, plus “Grant”/“Revoke” buttons.
          
          “Add User” form (modal): POST /api/users/ using the UserCreateSerializer (hashed password, cannot           set is_superuser via frontend). On success, table re‐loads.
          
          3. Products List (React)
          
          /pages/products-list route (all authenticated users).
          
          Calls GET /api/products/ to fetch product list (ID, name, description, price) and displays in a             Bootstrap table.
          
          Underneath, the comments area (uses <CommentList> and <CommentForm> components).
          
          4. Comments Components
          
          CommentList.jsx: Makes GET /api/comments/?page_id=1, lists each comment (username, timestamp,               content). Shows a “Delete” button if current user is the comment owner or a superuser.
          
          CommentForm.jsx: Simple textarea + “Post Comment” button. On submit, does POST /api/comments/               with { page:1, content:<text> }. On success, notifies parent to reloadComments.
          
          5. Permissions & ViewSets (Django)
          
          UserViewSet: superuser‐only (via IsSuperuser custom permission).
          
          PermissionViewSet: superuser‐only, managing page‐level permissions if/when used.
          
          PageListView: read‐only list of pages at /api/pages/.
          
          CommentViewSet: authenticated users only. For list(), filters by page_id query param.
          
          ProductViewSet: authenticated users only, CRUD on products at /api/products/.
          
          CommentHistoryListView: superuser‐only.

          6. Folder Structure Overview
 superadmin_proj/
├── backend/
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── …
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── …
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3    # (example SQLite database)
│
└── frontend/
    ├── node_modules/
    ├── public/
    │   ├── index.html
    │   └── …
    ├── src/
    │   ├── api/
    │   │   └── axiosInstance.js
    │   ├── components/
    │   │   ├── Auth/
    │   │   │   └── Login.jsx
    │   │   ├── Comments/
    │   │   │   ├── CommentList.jsx
    │   │   │   ├── CommentForm.jsx
    │   │   │   └── …
    │   │   ├── Dashboard/
    │   │   │   └── AdminDashboard.jsx
    │   │   ├── Pages/
    │   │   │   ├── ProductsListPage.jsx
    │   │   │   └── UsersPage.jsx
    │   │   └── Shared/
    │   │       └── Unauthorized.jsx
    │   ├── contexts/
    │   │   └── AuthContext.js
    │   ├── App.js
    │   ├── index.js
    │   └── …
    ├── package.json
    ├── package-lock.json
    └── README.md       # (if you want a separate frontend readme)

Challenges Faced & Solutions
1. JWT didn’t include is_superuser

Issue: The default TokenObtainPairSerializer only contains user_id.

Solution: Created MyTokenObtainPairSerializer (subclassed from TokenObtainPairSerializer) and added token["is_superuser"] = user.is_superuser (plus username). Configured SIMPLE_JWT["TOKEN_OBTAIN_PAIR_SERIALIZER"] in settings.py to point at this serializer.

2. React routing / redirect loops

Issue: After login, navigating to /admin sometimes immediately redirected to /login because AuthContext hadn’t yet fetched the full user object (and user.is_superuser was temporarily undefined).

Solution: In AuthContext, on mount if an access_token exists, immediately decode & fetch /accounts/user/<id>/. Only set user state after that call succeeds. Until then, components see user === null and show a loading spinner (or nothing). This prevented premature redirects.

3. Axios 404 errors (wrong URL prefixes)

Issue: Some API calls (e.g. /api/comments/) were pointing to /comments/ instead of including the /api/ prefix.

Solution: Centralized all API calls through axiosInstance (with baseURL: "http://127.0.0.1:8000/api/"). All components use relative paths (e.g. axiosInstance.get("comments/?page_id=1")).

4. Permission errors when fetching data

Issue: Non‐superusers could not fetch /api/users/ or /api/products/ because the viewsets were protected by the wrong permission class.

Solution:

UserViewSet: changed to permission_classes = [IsSuperuser] (custom DRF permission).

ProductViewSet: permission_classes = [permissions.IsAuthenticated].

CommentViewSet: permission_classes = [permissions.IsAuthenticated].

Elevated comments: superusers can see all comment history; regular users only see their own page’s comments.

5. “Cannot destructure ‘user’ of undefined” in React

Issue: In App.js, calling useContext(AuthContext) outside of an <AuthProvider> wrapper caused user to be undefined.

Solution: Moved <AuthProvider> into index.js (wrapping <App /> inside <BrowserRouter>, <AuthProvider>). Now any component using useContext(AuthContext) sees a valid context.
