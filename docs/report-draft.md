# Consultant Management System

Graduation Project Report — Week 2 Draft

## 1. Introduction

Many companies work with consulting firms, and this number is growing every day. Working with a consulting firm is often cheaper, and the company does not have to manage salary payments or insurance for each person. Companies can also choose the best firm and end the collaboration whenever they want.

## 2. Problem Statement

Planning between companies and consultants is still done through meetings and manually prepared schedules. The problem is that there are many restrictions. For example, one consultant does not work on Mondays and Thursdays, and the same consultant is not available on Friday of the following week. The person who prepares the schedule has to keep all of this information in mind.

## 3. Motivation

My goal is to add these restrictions to a system and make this planning much easier. In this way, mistakes will be reduced, and the process will be quicker and easier.

## 4. Project Objective

I want to develop an internal web application. The person who prepares the schedule will manage all of these restrictions in one place. People from the consulting firm will be able to see their tasks on a calendar and follow their work easily.

The system will have three types of users:

- The admin who manages the system
- The person who prepares the schedule
- Consultant firm workers

## 5. Preliminary Scope

### 5.1 Included in the first version

- Managing the restrictions of consultants
- A calendar where consultants can see their tasks

### 5.2 Not included in the first version

- In the future, the system may also send calendar invitations automatically.
- AI agents are becoming very popular. In the future, I want to add an AI agent that can manage restrictions easily. For example, restrictions could be managed through voice chat, and the agent would update the calendar automatically.

## 6. Requirements Analysis

### 6.1 Review of the Week 1 Definition

**Who is the primary user or stakeholder?**
The primary users are the people in the company who plan the work, and the consultants from the consulting firms who do the work. The system is not limited to one field: any department that works with a consulting firm, such as IT, accounting or human resources (for example for payroll), can use it. Other stakeholders are the consulting firms themselves and the company management, because they are affected by how the consultants' time and budget are used.

**What specific problem does this user have?**
As described in the problem statement, planning is done through meetings and manually prepared schedules. The planner has to remember many restrictions for each consultant, and this causes mistakes and misunderstandings.

**What is the single most important result?**
To make the planning process easier by turning it into an automated system. The planner can plan much more easily because the system checks the restrictions, and each consultant can see their own work clearly.

**Which features are essential for the first prototype?**
The tasks that are assigned must be shown correctly in a table. Small bugs are acceptable at this stage, but the main structure must work so that it can be shown to a user. Login, the calendar view and the .ics download can wait.

**Checkpoint**
The system is used by planners in companies that work with consulting firms, and by the consultants of these firms. Today, planning is done through meetings and manually prepared schedules, so the planner has to keep many restrictions in mind, such as working days, leave days, a weekly day limit and a monthly budget limit. This leads to mistakes and misunderstandings between the company and the consulting firm. The first version will let the planner assign tasks while the system checks these restrictions automatically, and it will show the assigned tasks in a table. Compared to Week 1, two things changed: a third user role (the planner) was added, and the restrictions were defined more clearly as four types.

### 6.2 User Roles

*Table 1: User roles*

| Role | Description |
|---|---|
| Admin | Manages the system and creates departments and planner accounts. |
| Planner | Manages consultants, restrictions and task assignments in one department. |
| Consultant | Views only their own tasks on a read-only calendar. |

## 7. Functional Requirements

*Table 2: Functional requirements*

| ID | Requirement statement | Priority |
|---|---|---|
| FR-01 | The system shall allow a user to log in with a username and password and shall show only the pages allowed for the user's role (admin, planner or consultant). | Must |
| FR-02 | The system shall allow the admin to create a department. | Must |
| FR-03 | The system shall allow the planner to add a consultant with working weekdays, a weekly day limit and a monthly budget limit (in days). | Must |
| FR-04 | The system shall allow the planner to add leave days for a consultant. | Must |
| FR-05 | The system shall reject a task assignment that falls on a non-working day or a leave day, or exceeds the weekly limit or the monthly budget, and shall display the reason. | Must |
| FR-06 | The system shall display a consultant's assigned tasks on a read-only calendar for that consultant. | Should |
| FR-07 | The system shall allow a consultant to download their calendar as an .ics file. | Could |

## 8. Non-Functional Requirements

*Table 3: Non-functional requirements*

| ID | Quality | Requirement | How to verify |
|---|---|---|---|
| NFR-01 | Security | User passwords shall be stored only as salted hashes, never as plain text. | Inspect the database after creating a user; an automated test checks that the stored value is different from the password. |
| NFR-02 | Security / data isolation | A planner shall not be able to view or change data that belongs to another department. | An automated test logs in as a planner of department A and checks that requests for department B data are rejected. |
| NFR-03 | Performance | The calendar of one department with 50 consultants for one month shall load within 2 seconds on the development laptop. | Measure the API response time with test data of 50 consultants. |

## 9. Scope, Constraints and Assumptions

*Table 4: Scope, constraints and assumptions*

| Category | Item |
|---|---|
| In scope | Login with three roles (admin, planner, consultant) |
| In scope | Managing departments, consultants and their four restriction types |
| In scope | Task assignment with automatic restriction check |
| In scope | Read-only calendar for consultants |
| Out of scope | Automatic e-mail or calendar invitations |
| Out of scope | AI agent for managing restrictions by voice or chat |
| Out of scope | Mobile application and Excel import |
| Constraint | The project must be completed in nine weeks by one developer. |
| Constraint | The developer is learning React during the project. |
| Constraint | Development and testing are done on one personal laptop. |
| Assumption | Users have a modern web browser and access to the company network. |
| Assumption | Each consultant belongs to only one department. |

The most important limitation is time. For this reason, the first version focuses on the restriction check, which is the core value of the system. Docker-based installation and live deployment will be added only if time allows.

## 10. User Stories

**US-01 — Blocking an invalid assignment** (FR-05)
As a planner, I want the system to stop me when I assign a task to a consultant on a day they cannot work, so that I do not create a wrong schedule.

Acceptance criteria:
1. Given a consultant who is on leave on 14 October, when the planner assigns a task on that day, the task is not saved.
2. The system displays the reason, for example "Consultant is on leave on 2026-10-14".

**US-02 — Respecting the monthly budget** (FR-03, FR-05)
As a planner, I want the system to count the days already assigned in a month, so that the budget agreed with the consulting firm is not exceeded.

Acceptance criteria:
1. Given a consultant with a monthly budget of 8 days and 8 assigned days in October, when the planner assigns a 9th day in October, the task is not saved and the reason is displayed.
2. When the planner assigns a task in November for the same consultant, the assignment is accepted.

**US-03 — Viewing my own tasks** (FR-01, FR-06)
As a consultant, I want to see my tasks on a calendar, so that I know where and when I work without asking the planner.

Acceptance criteria:
1. When a consultant logs in, the calendar shows only the tasks assigned to that consultant.
2. The consultant cannot create, change or delete any task.

## 11. Development Plan

*Table 5: Development plan*

| Week | Project-specific milestone |
|---|---|
| Week 3 | Architecture diagram, database tables (departments, users, consultants, leave days, tasks) and API endpoint list |
| Week 4 | Prototype: the planner can add a consultant and assign tasks, invalid assignments are rejected with a reason, and the assigned tasks are shown in a table |
| Week 5 | Login with three roles, department data isolation and the first React screens (consultant list, task assignment) |
| Week 6 | Read-only consultant calendar and automated tests for all four restrictions and for data isolation |
| Week 7 | Installation guide with requirements files; .ics download; Docker setup and live demo if time allows |
| Week 8 | Report completion, professional README and screenshots |
| Week 9 | Final demonstration and presentation |
