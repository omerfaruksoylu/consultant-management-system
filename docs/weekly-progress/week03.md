# Week 3 Progress Log

| Field | Student response |
|---|---|
| Tasks planned and completed | Reviewed Week 2 requirements; defined system components; prepared the architecture diagram; described one end-to-end flow (task assignment); designed the database tables; recorded two technology decisions; identified two risks; defined the Week 4 prototype goal. |
| New diagrams / files | `docs/design/architecture.png`, `docs/design/architecture.drawio` (editable source), `docs/weekly-progress/week03.md`; report section 12 (Methodology and System Design) and References. |
| GitHub commit links or hashes | https://github.com/omerfaruksoylu/consultant-management-system/commit/46d3706 |
| Technical problems found | Building a separate React frontend would take too much time for one developer in nine weeks. The .ics calendar download was not essential for the first version. |
| Solutions considered | React frontend vs. server-rendered Jinja2 templates; PostgreSQL vs. SQLite. Selected Jinja2 templates and SQLite (report Table 10, ADR-01 and ADR-02). |
| References consulted | FastAPI documentation (Templates page), SQLite "Appropriate Uses For SQLite", React documentation, Van den Bergh et al. (2013), Panko (2015). |
| Report sections updated | Title page information; in-text citations in sections 2 and 3; FR-07 removed; Tables 1–5 explained in the text; new section 12 (12.1–12.9); References section. |
| Changes to earlier decisions | 1) User interface: React was replaced by server-rendered HTML pages with Jinja2 templates, so the whole system stays in one language (Python) and one project (ADR-01). 2) FR-07 (calendar download as an .ics file, priority Could) was removed from the first version. 3) The constraint "the developer is learning React" was replaced by "the developer is also attending another intensive training programme". Reason for all changes: keeping the project realistic for one developer within nine weeks. The Must requirements did not change. Details: report section 12.9. |
| Week 4 prototype objective | Demonstrate a task assignment page where the planner's form passes through FastAPI and the restriction check module to produce either a new row in the task table or a rejection message with the reason. Evidence: screenshots of both cases and test output. |
