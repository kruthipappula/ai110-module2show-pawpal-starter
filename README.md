# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Owner: Jordan
Pets:
- Mochi (dog)
- Whiskers (cat)
Today's Schedule:
07:30 - Feed breakfast (daily)
08:00 - Morning walk (daily)
18:00 - Dinner (daily)


## 🧪 Testing PawPal+

Run the test suite: 

```bash
python -m pytest
```
**What the tests cover:**
-Task completion behavior
-Adding tasks to a pet
-Sorting tasks by scheduled time
-Filtering tasts by pet and completion status
-Recurring task creation (daily and weekly)
-Conflict detection for overlapping tasks

**Confidence:** ★★★★☆ (4/5) — checks the main scheduling features and behavior; still additional edge cases that could be tested, such as tasks crossing midnight, more complex recurring schedules, and larger numbers of pets and tasks

Sample test output:

```
PS C:\Users\srikr\OneDrive\Desktop\.vscode\CodePath\ai110-module2show-pawpal-starter> python -m pytest
========================================================================================= test session starts ==========================================================================================
platform win32 -- Python 3.13.0, pytest-9.1.0, pluggy-1.6.0
rootdir: C:\Users\srikr\OneDrive\Desktop\.vscode\CodePath\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 19 items                                                                                                                                                                                      

tests\test_pawpal.py ...................                                                                                                                                                          [100%]

========================================================================================== 19 passed in 0.08s ==========================================================================================                                                                        python -m pytest:\Users\srikr\OneDrive\Desktop\.vscode\CodePath\ai110-module2show-pawpal-starter> 
====================================== test session starts ======================================
platform win32 -- Python 3.13.0, pytest-9.1.0, pluggy-1.6.0
rootdir: C:\Users\srikr\OneDrive\Desktop\.vscode\CodePath\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 19 items                                                                               

tests\test_pawpal.py ...................                                                   [100%]

====================================== 19 passed in 0.09s =======================================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | 'Scheduler.sort_by_time()' | Sorts tasks in chronological order based on their scheduled time. |
| Filtering | | 'Scheduler.filter_tasks()' | Filters tasks by pet name or completion status (completed or pending). |
| Conflict handling | | 'Scheduler.find_conflicts()', 'Scheduler.describe_conflicts()' | Detects overlapping task times and displays warning messages instead of interrupting the program. |
| Recurring tasks | | 'Task.next_due_date()', 'Task.next_occurence()', 'Scheduler.complete_task()' | Automatically creates the next occurence of daily and weekly tasks after they are completed. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
