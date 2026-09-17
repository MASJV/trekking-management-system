# Trekking Management System
A role-based trekking management application for managing treks, staff assignments, user bookings, payments, and the trek lifecycle through dedicated Admin, Trek Staff, and Trekker workflows.

Developed as part of the Modern Application Development I (MAD1) project at IITM.

Project Statement: [View Project Statement](https://docs.google.com/document/u/3/d/e/2PACX-1vQvgzwz2tFt96B8VApnHqWqlP3LtPDbnxYwAPyr8VOffLCm_Zh2JuTa51z7d1CNJbrZKC0oWPredYcV/pub)

Demo Video: [Watch Project Demo](https://drive.google.com/file/d/1lPMqAqLAwftx0PELTpIJrgMJtcimAC1c/view?usp=sharing)

**Project Grade:** S — 90/100

---

## Run Locally

Clone the repository:

```bash
git clone https://github.com/MASJV/trekking-management-system.git
cd trekking-management-system
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the application in your browser at:

```text
http://127.0.0.1:5000
```

The SQLite database and required tables are created automatically when the application starts.

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

Booking records and trek completion details visible to Admin.  

Booking allowed only when trek status is Open, and blocked once slots are full. (prevents overbooking)

Maintain trek booking statuses (Booked / Cancelled / Completed).
On cancelling, the booking is soft-cancelled (recorded not deleted just marked  and slot is freed)
On rebooking a cancelled trek, the same booking row is utilized instead of making a duplicate.  
When a trek is marked Completed, all of its non-cancelled bookings are marked Completed as well.  

Trek status tracking maintained (Pending / Approved / Open / Closed / Completed).  

Bugs faced & fixed:  
    - Earlier cancelling deleted the booking row so Cancelled history was lost -> switched to soft-cancel (only status changed to cancelled).    
    - Participant list and trekker counts were also counting cancelled bookings -> filtered them out.  
    - Cancelling an already cancelled booking inflated available slots -> added a safety guard.  
    - Staff dashboard trekker count compared the bookings list to a string and updated the wrong variable -> fixed to count booking.status correctly.  

---

### CORE MILESTONES COMPLETED.

### 9th July, 2026
**Additional Milestone Completed: Flask-Login Integration**  

Integrated Flask-Login.

Restricted routes based on roles.

Implemented template inheritance for better design choice.

---

### 11th July, 2026
**Additional Milestone Completed: Frontend and Backend Validation**  

Added HTML5 frontend validation (required fields, email type, number min, 10-digit phone length).  

Added backend validation in routes:  
    Staff phone number must be exactly 10 digits.  
    Trek end date cannot be before start date -> it would show an error message instead of a silent redirect.  

UX fixes:  
    Full treks(0 slots) are no longer shown under available/open treks.  
    Booked Treks page shows only active bookings, completed ones move to Trekking History.  
    Fixed logout button positioning.

---

### 13th July, 2026

Added Images corresponding to each trek detail. 

Fixed a silly mistake which prevented the details beside image to fill up, leaving plain spaces around it.

Dug out a few fields that were sitting in the database doing nothing — Admin now sees each staff's phone number and treks-completed count, staff see their own completed count, and users can finally see which guide is taking them (and how many treks that guide has completed so far).

Caught another silly one — a staff could mark a trek Completed, reopen it, complete it again and farm the count like loyalty points. Made the count symmetric instead: completing adds one, reopening (say, a mis-click) takes it back and restores the bookings.

Fixed minor bugs, better configuration.