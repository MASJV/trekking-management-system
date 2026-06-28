# trekking-management-system
A Trekking Management app where Admin, Trek Staff and Users manage treks, staff assignments and bookings by role.

---

### 19 Jun 2026  
**Milestone 1 Completed: Database Models and Schema Setup**  
Created models for admin, user, trek, booking and staff.

These database tables are created programatically using python not manually.  

Established relationships wherever required.  
ie.  
A User can have multiple Bookings.  
A Staff can be assigned to multiple treks.
A Trek can have multiple Bookings.

---

### 20 Jun 2026  
**Milestone 2 Completed: Authentication and Role Based Access**  
Implemented Admin login.

Implemented User(Trekker) and Staff registration + login 

Established role-specific dashboards + Restrict dashboard access based on user roles.

---

### 28 Jun 2026  
**Milestone 3 Completed: Admin Dashboard and Management**  
Implemented Admin dashboard with live counts of treks, users, staff and bookings.

Built create, edit, delete and a filter(by ID, name, difficulty, location, status).

Added User management with name search and blacklist/unblacklist.

Added Staff management with approve, unapprove, and delete + staff to trek assignment(only approved and active staff are assignable).

Unapproving or deleting a staff revokes their trek assignments.

---