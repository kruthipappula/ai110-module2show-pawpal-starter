# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design focused on the main aspects to the PawPal+ system: the Owner, Pet, Task, and Scheduler classes. The goal was to create a system where users could add and manage information about themselves and their pets. Users should also be able to create and manage pet care tasks such as feeding, walks, mediciations, grooming, and appointments. Lastly, users should be able to view a daily schedule that organizes all of their pet care tasks. I wanted each class to have its own responsibility so the system stays organized and is easy to understand.

- What classes did you include, and what responsibilities did you assign to each?

For the UML design, I included four main classes: Owner, Pet, Task, and Scheduler. The Owner class stores information about the pet owner and manages their list of pets. The Pet class contains information about each pet, such as its name, species, and assigned care tasks. Its methods allow users to add tasks and view their pet's tasks. The Task class represents a pet care activity and stores information like the task description, scheduled time, duration, frequency, and where it has been completed or not. The Scheduler class collects tasks from all of the owner's pets, organizes them into a daily schedule, sorts them by time, filters tasks, and checks for scheduling conflicts. 

**b. Design changes**

- Did your design change during implementation? Yes
- If yes, describe at least one change and why you made it.

One change that was made after reviewing the class skeleton was improving the relationship between the Owner and Scheduler classes. My original idea was to include extra information such as owner preferences and task priority, but then I realized they weren't necessary for the basic requirements of this project. I also made the relationship between the Owner and Scheduler classes clearer by having the Scheduler get tasks directly from the owner's pets. This made the design more consistent with the UML diagram that was generated while keeping the system simple. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler considers the scheduled time, task duration, recurring schedules, task status, and the pet each task belongs to. It sorts tasks by time, filters tasks by pet or completion status, and checks for overlapping task times so conflicts can be displayed to the user.

- How did you decide which constraints mattered most?

I decided that time and duration were the components that mattered the most since the purpose of the scheduler was to organize pet care tasks. I also included filtering and conflict detection because they make the schedule easier to read and help users identify overlapping tasks. I chose not to include more advanced features like scheduling based on priority to keep the system simple. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

One tradeoff my scheduler makes is that it warns the user about scheduling conflicts but does not automatically rearrange tasks to fix the problem.

- Why is that tradeoff reasonable for this scenario?

I think this tradeoff is reasonable because every pet owner might want to handle scheduling conflicts differently. By displaying a warning, the user is alerted and can decide how to adjust their schedule and personalize their schedule according to their needs.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used Claude throughout the project to help brainstorm my UML design, create the class skeleton, debug logic errors, improve my scheduler, and implementing methods like sorting, filtering, and conflict detection. 

- What kinds of prompts or questions were most helpful?

The most helpful prompts were the ones asking Claude to explain why something worked and reviewing my code for improvements as it provided beginner-friendly implementations of certain features.  

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

One moment I did not accept and AI suggestion as-is was when Claude generated a complex UML diagram initially. It suggested adding more attributes and methods than was necessary so I changed the design slightly to make it easy to understand. 

- How did you evaluate or verify what the AI suggested?

I evaluated the suggestions by reviewing the code and testing it. Using separate chat sessions helped me stay organized because I could focus on one part of the project at a time. I was also able to simplify the logic to make it easier to read and maintain, while still ensuring it worked correctly by running the app and tests. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested task completion, adding tasks to pets, sorting tasks by scheduled time, filtering tasks by pet and completion status, recurring task creation, and conflict detection.

- Why were these tests important?

These tests helped verify that the main features of the scheduler worked correctly. They also helped me catch any bugs before connecting everything to the Streamlit app and gave me more confidence that the system behaved as expected.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am fairly confident that my scheduler works correctly because all of my automated tests passed successfully and I was able to test the app through both the command line and the Streamlit interface.

- What edge cases would you test next if you had more time?

If I had more time, I would test tasks that cross midnight, more complicated recurring schedules, and having larger lists of pets and tasks to make sure the system still behaves correctly.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the scheduler because it brings together all of the classes and makes the application functional. I also liked the sorting, filtering, recurring tasks, and conflict detection features because they made the scheduler more useful.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would try to improve the scheduler by adding more complex priority-based scheduling or automatic conflict resolution so that pet and task information could be saved between sessions.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned is that planning the system before writing code made the implementation much easier. I also learned that Claude did a pretty good job of brainstorming, debugging, and reviewing ideas, but it was still critical for me to evaluate its suggestions and make final decisions myself.
