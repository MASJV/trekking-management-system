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

### 2nd July 2026  
**Milestone 4 & 5 Completed: Trek Staff Dashboard and Trek Management, User Dashboard and Trek Booking System**  

Added following to Staff functionalities/Dashboard:  
    Staff can register, login and edit his/her profile.  
    Staff can access and manage only their assigned treks.  
    Staff dashboard shows assigned treks count and total registered trekkers count.  
    Staff can update available trek slots and trek status(open, closed, started, ongoing, completed).  
    Staff can view and manage the participant list of assigned treks(remove a participant frees a slot).  
    Only the assigned staff can manage a given trek.  

Added following to User(Trekker) functionalities/Dashboard:  
    User can register, login and edit his/her profile.  
    User can view available/open treks and filter them by difficulty and location.  
    User can book a trek and track its booking status.  
    User can view booked treks, trek status and trekking history.  
    Duplicate bookings are prevented, and booking is blocked when a trek is full or closed.  

Added a payment_status field to Booking; Admin marks payment as paid/pending(offline payment).  

Booking or removing a participant will keep available slots in sync automatically.  

---