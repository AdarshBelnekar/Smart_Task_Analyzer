# Task Analyzer System – Project Documentation

##  Overview
This project implements a Task Prioritization System that assigns a priority score to each task based on weighted parameters such as urgency, importance, due dates, and estimated effort. Users can add tasks, view their priority levels, and understand how the scoring algorithm ranks tasks.

---

##  Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/AdarshBelnekar/Smart_Task_Analyzer.git
```

### Create the backend and frontend folder 
* In backend
  ```bash
  python -m venv venv
   ```
   * Run the requirnment file
     ```bash
       pip install -r requirements.txt
       ```

  * Run Migration
    ```bash
    python manage.py makemigrations
    python manage.py migrate
     ```
  * Start Django development server:
    ```
    Start Django development server:
    ```
* Frotned
   - Simply run the html page.    
     
# Algorithm Explanation:
The goal of the algorithm is to assign every task a numeric score that represents how important it is compared to other tasks.
#### Priority Scoring Algorithm
The algorithm calculates a Priority Score for each task using four factors:

Urgency Score:    Calculated based on the number of days remaining until the due date. Past-due tasks are treated as urgent (negative days counted as positive for urgency).

Importance Score:  User-provided rating from 1 to 10.

Effort Score: Lower effort tasks are considered "quick wins."
Computed as max_effort - task.estimated_hours to prioritize easier tasks.

Dependency Score:  Tasks that block other tasks receive additional weight.( Computed as the number of tasks dependent on this task) .

## Final Formula (Weighted) :

* Priority Score = (Importance × 2.5) + (Effort × 1.5) + (Urgency × 3) + (Dependencies × 2)


### The algorithm is configurable to support multiple strategies:

* Fastest Wins – prioritize low-effort tasks

* High Impact – prioritize high importance

* Deadline Driven – prioritize urgent tasks

* Smart Balance – custom balance of all factors
## Design Decisions

Weights: Chosen to balance urgency, importance, effort, and dependencies.

Overdue Tasks: Urgency score adjusted to penalize negative days.

Missing/Invalid Data: Task skipped and logged, API returns error message.

Circular Dependencies: Detected and reported, visualization optional.

Frontend simplicity: Single-page UI with clean table and top 3 recommendations

## Time Spend (Approx).

| Task                            | Time Spent |
| ------------------------------- | ---------- |
| Backend Models & API            | 120 min     |
| Priority Algorithm Development  | 60  min     |
| Frontend UI & JS Integration    | 60 min     |
| Unit Tests & Debugging          | 30 min     |
| Bonus Features (Circular Graph) | 45 min     |

## Future Improvement 
- Add more Visulatization (Graph,matrix,etc).
- Admin functionality with database.

- Implements Date adding holidays.
