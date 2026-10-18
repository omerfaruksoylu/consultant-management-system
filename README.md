# Consultant Management System

Constraint-Aware Scheduling for Departments Working with Consulting Firms

## Project Description

Many companies work with consulting firms, and this number is growing every day. Working with a consulting firm is often cheaper, and the company does not have to manage salary payments or insurance for each person. Companies can also choose the best firm and end the collaboration whenever they want. However, planning between companies and consultants is still done through meetings and manually prepared schedules. The problem is that there are many restrictions. For example, one consultant does not work on Mondays and Thursdays, and the same consultant is not available on Friday of the following week. The person who prepares the schedule has to keep all of this information in mind. My goal is to add these restrictions to a system and make this planning much easier. In this way, mistakes will be reduced, and the process will be quicker and easier.

## Objective

I want to develop an internal web application. The person who prepares the schedule will manage all of these restrictions in one place. People from the consulting firm will be able to see their tasks on a calendar and follow their work easily.

## Target Users

- **Admin:** manages the system and creates departments
- **Planner:** manages consultants, restrictions and task assignments in one department
- **Consultant:** views their own tasks on a read-only calendar

## Planned Features

- Login with three roles: admin, planner and consultant
- Department management
- Consultant management with four restriction types:
  - working weekdays
  - leave days
  - weekly day limit
  - monthly budget limit (in days)
- Task assignment with an automatic restriction check
- Read-only calendar for consultants
- Calendar download as an .ics file

## Scope

**Included in the first version:** login and roles, departments, consultants and restrictions, task assignment with restriction check, consultant calendar.

**Not included in the first version:** automatic e-mail invitations, AI agent, mobile application, Excel import.

## Planned Technologies

- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite
- **Frontend:** React
- **Testing:** pytest
- **Deployment:** Docker (if time allows)

## Requirements

Functional and non-functional requirements are listed in the Graduation Project Report (sections 7 and 8).

## Current Status

Week 2 - Requirements analysis and planning.

- [x] Project definition, references and initial report (Week 1)
- [x] Functional and non-functional requirements
- [x] Scope, constraints, assumptions and user stories
- [x] Development plan and GitHub Issues
