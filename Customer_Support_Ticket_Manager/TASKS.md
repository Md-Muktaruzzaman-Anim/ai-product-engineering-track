# Tasks 1–15: How the final project maps to the learning roadmap

The `main.py` file is the consolidated final version, not 15 separate copies of the same script. Build it incrementally using the task mapping below.

1. **Create and persist one ticket** — `create_ticket()` and `save_tickets()`.
2. **Read a ticket from JSON** — `load_tickets()` and `find_ticket()`.
3. **Keep multiple tickets** — the JSON file stores a list of ticket dictionaries.
4. **Display all tickets** — `print_tickets()` and `print_ticket()`.
5. **Add without losing existing tickets** — load the list, append a ticket, then save the whole list in `create_ticket_from_input()`.
6. **Generate ticket IDs** — `get_next_ticket_id()`.
7. **Get customer information from input** — `create_ticket_from_input()`.
8. **Search by ID** — `find_ticket()` and `search_ticket()`.
9. **Update status** — `update_ticket_status()` and `change_ticket_status()`.
10. **Filter by status or priority** — `filter_tickets()` and `filter_ticket_menu()`.
11. **Delete a ticket** — `delete_ticket()` and `delete_ticket_menu()`.
12. **Handle errors and invalid input** — validation in `prompt_ticket_id()`, `load_tickets()`, `create_ticket()`, `filter_tickets()`, and the `try/except` in `main()`.
13. **Refactor into reusable functions** — the core behaviour is separated into small functions throughout `main.py`.
14. **Automated tests** — `test_main.py`; run them using `python -m pytest -q`.
15. **Documentation and final verification** — `README.md`; run the app and its tests before moving on.

## Suggested practice

Even though the final code is available, do not just copy it and move on. Read one function at a time, explain what it does in your own words, then temporarily change or rebuild it yourself. Before beginning FastAPI, be able to explain how data is loaded, modified, and saved, and why the tests pass.
