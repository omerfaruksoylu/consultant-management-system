# Consultant Management System

Constraint-Aware Scheduling for Departments Working with Consulting Firms

## Project Description

Many companies work with consulting firms. Working with a consulting firm is often cheaper, and the company does not have to manage salary payments or insurance for each person. Companies can also choose the best firm and end the collaboration whenever they want. However, planning between companies and consultants is still done through meetings and manually prepared schedules. The problem is that there are many restrictions. For example, one consultant does not work on Mondays and Thursdays, and the same consultant is not available on Friday of the following week. The person who prepares the schedule has to keep all of this information in mind. My goal is to add these restrictions to a system and make this planning much easier. In this way, mistakes will be reduced, and the process will be quicker and easier.

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
- Read-only task view for consultants

## Scope

**Included in the first version:** login and roles, departments, consultants and restrictions, task assignment with restriction check, consultant calendar.

**Not included in the first version:** automatic e-mail invitations, AI agent, mobile application, Excel import.

## Planned Technologies

- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite
- **Frontend:** Server-rendered HTML pages with Jinja2 templates
- **Testing:** pytest
- **Deployment:** Docker (if time allows)

## Requirements

Functional and non-functional requirements are listed in the Graduation Project Report: [docs/report-draft.md](docs/report-draft.md) (sections 7 and 8).

## Architecture

The user works in a web browser. The browser sends requests to a FastAPI application on the server. FastAPI checks the login and department, runs the restriction check, reads and writes data in a SQLite database, and returns HTML pages created with Jinja2 templates.

![System architecture](docs/design/architecture.png)

Details: Graduation Project Report, section 12.

## Repository Structure

```
consultant-management-system/
├── README.md                     # Project overview (this file)
├── .gitignore
└── docs/
    ├── report-draft.md           # Graduation Project Report (updated every week)
    ├── project-description.md    # Week 1: project description
    ├── references.md             # Week 1: academic and technical references
    ├── design/
    │   ├── architecture.png      # Week 3: system architecture diagram
    │   └── architecture.drawio   # Week 3: editable diagram source (draw.io)
    └── weekly-progress/
        └── week03.md             # Week 3: progress log
```

The application code (`backend/`) will be added from Week 4.

## Current Status

Week 3 - Architecture and technical design.

### Week 1 - Project definition and research
- [x] Project idea, problem and objective defined
- [x] Initial README created
- [x] Academic and technical references reviewed
- [x] Initial report sections drafted

### Week 2 - Requirements analysis and planning
- [x] Functional and non-functional requirements
- [x] Scope, constraints, assumptions and user stories
- [x] Development plan and GitHub Issues

### Week 3 - Architecture and technical design
- [x] Architecture diagram, components and system boundaries
- [x] End-to-end data flow and database design
- [x] Technology decisions (SQLite, server-rendered templates)
- [x] Report updated with system design and references

### Next
- [ ] Week 4 - First working prototype
