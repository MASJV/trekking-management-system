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

Bug faced & fixed:  
    - Assigned Trek IDs column showed merged wrong output (eg "53" instead of "3,5") due to wrong join syntax -> fixed by building the id string correctly.

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

Bugs faced & fixed:  
    - Marking a trek Completed crashed as it used trek.assigned_staff which does not exist -> used the correct relationship, and validated the end date before updating status.  
    - Trek statuses Started/Ongoing were not selectable in the dropdown -> added them.

---

### 5th July, 2026
**Milestone 6 Completed: Trek Booking History and Trek Status Tracking**  

Maintained complete trekking history per user (booked + completed treks).  

Booking records and trek completion details visile to Admin.  

Booking allowed only when trek status is Open, and blocked once slots are full. (prevents overbooking)

Maintain trek booking statuses (Booked / Cancelled / Completed).
On cancelling, the booking is soft-cancelled (recored not deleted just marked  and slot is freed)
On rebooking a cancelled trek, the same booking row is utilized instead of making a duplicate.  
When a trek is marked Completed, all of its non-cancelled bookings are marked Completed as well.  

Trek status tracking maintained (Pending / Approved / Open / Closed / Completed).  

Bugs faced & fixed:  
    - Earlier cancelling deleted the booking row so Cancelled history was lost -> switched to soft-cancel (only status changed to cancelled).    
    - Participant list and trekker counts were also counting cancelled bookings -> filtered them out.  
    - Cancelling an already cancelled booking inflated available slots -> added a safety guard.  
    - Staff dashboard trekker count compared the bookings list to a string and updated the wrong variable -> fixed to count booking.status correctly.  

---