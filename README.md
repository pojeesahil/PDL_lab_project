# 🛡️ ClashAudit — Faculty Workload Distribution & Conflict Detector
> **Python Data Lab (PDL) Mini Project** | Intelligent Timetable Conflict Detection, Workload Balancing & ML Burnout Risk Prediction

An institutional operations dashboard engineered to automate academic timetable conflict detection, enforce AICTE/UGC workload limits, balance departmental teaching hours, and predict faculty burnout risk using machine learning.

---

## 📌 Problem Statement

In academic institutions (engineering colleges & universities), scheduling hundreds of courses and lab sections across various departments is a high-dimensional constraint satisfaction challenge. Manual or static timetable generation frequently leads to:
1. **Faculty Time Collisions**: Same professor scheduled for two different classes at the identical time slot.
2. **Room Double-Booking**: Two distinct courses scheduled in the same lecture hall or laboratory simultaneously.
3. **Faculty Fatigue & Burnout**: Consecutive teaching streaks (≥ 4 hours without rest) and disproportionate weekly teaching assignments violating statutory quotas.
4. **Unbalanced Resource Utilization**: Junior faculty overloaded (20+ hrs) while senior faculty remain underutilized, violating AICTE/UGC institutional governance.

**Objective**: Develop a clean, lightweight, and demonstratable system with:
- An **algorithmic conflict detector** that scans any timetable schedule in real-time, highlights hard and soft conflicts, and calculates a departmental **Workload Balance Index (WBI)**.
- A **smart auto-reassignment engine** that discovers eligible substitute faculty in the same department to eliminate collisions in one click.
- A **supervised Machine Learning classifier (96.25% test accuracy)** that predicts faculty stress/burnout risk based on teaching, lab, administrative, and research hours.
- A **clean, responsive Web UI (HTML5, CSS3, JavaScript)** featuring **instant one-click demo scenarios** designed for university lab vivas and presentations.

---

## 🏛️ Academic Workload Norms (AICTE / UGC Guidelines)

| Academic Designation | Direct Teaching (Lectures) | Lab / Practical Sessions | Administrative & Research | Max Weekly Cap |
|---|---|---|---|---|
| **Assistant Professor** | 12 – 14 hrs/week | 4 – 6 hrs/week | 2 – 4 hrs/week | **18 Hours / Week** |
| **Associate Professor** | 8 – 10 hrs/week | 2 – 4 hrs/week | 4 – 6 hrs/week | **16 Hours / Week** |
| **Professor / HOD** | 4 – 6 hrs/week | 0 – 2 hrs/week | 6 – 8 hrs/week | **14 Hours / Week** |

---

## ⚙️ Machine Learning Model Evaluation & Benchmarking

We synthesized a realistic institutional dataset of **400 faculty members** (`dataset/faculty_workload.csv`) across Computer Science, Information Technology, AI & Data Science, and Electronics departments.

We evaluated four candidate models using stratified 80/20 train-test splits and 5-fold cross-validation:

| Model Architecture | Test Accuracy | Precision | Recall | F1-Score | 5-Fold Stratified CV |
|---|---|---|---|---|---|
| **Logistic Regression (Selected)** | **96.25%** | **96.48%** | **96.25%** | **96.24%** | **95.50%** |
| Decision Tree Classifier | 93.75% | 94.10% | 93.75% | 93.76% | 90.00% |
| Random Forest Classifier | 91.25% | 91.45% | 91.25% | 91.19% | 92.25% |
| Gaussian Naive Bayes | 48.75% | 52.10% | 48.75% | 41.16% | 53.50% |

### Why Logistic Regression?
- **High Accuracy & Generalization**: Highest accuracy (96.25%) and tightest 5-fold CV score (95.50%).
- **Simplicity & Interpretability**: Clean multi-class decision boundaries with zero black-box obscurity.
- **Fast CPU Inference**: Execution time < 1 ms with negligible memory overhead.

---

## 🖥️ Web User Interface Features

- **Instant Demo Scenarios (One-Click Viva Presets)**:
  - 🟢 **Scenario A: Optimal Timetable**: 0 conflicts, balanced distribution across all departments.
  - 🔴 **Scenario B: Critical Collisions**: Faculty time clash (Dr. Rajesh Sharma scheduled in two classes at Monday 10:00 AM) + Room clash (LH-101 double-booked on Wednesday).
  - 🟡 **Scenario C: Overload & Fatigue**: 4 back-to-back continuous hours + 20+ weekly hours on Dr. Amit Verma.
- **1-Click AI Auto-Resolve**: Generates alternative assignment options and swaps conflicted faculty with an available, qualified peer in one click.
- **Live Timetable Grid**: Interactive table with status badges (`Clash` / `Valid`) and inline test session addition.
- **Faculty Workload Utilization Meters**: Visual progress bars tracking hours against AICTE thresholds (Green: Balanced, Amber: Underloaded, Red: Overloaded).
- **Interactive ML Burnout Calculator**: Allows testing individual faculty combinations to view multi-class stress probabilities and institutional guidance.

---

## 📁 Directory Structure

```
PDL_lab_project/
├── dataset/
│   ├── faculty_workload.csv        # 400 faculty academic dataset
│   └── generate_dataset.py         # Reproducible dataset generator
├── model/
│   ├── train.py                    # Multi-model benchmarking script
│   ├── workload_model.joblib       # Trained production inference model
│   └── model_metadata.json         # Metrics, odds ratios & guidelines
├── core/
│   ├── conflict_detector.py        # Algorithmic collision & fatigue engine
│   └── scenarios.py                # Preconfigured demo institutional scenarios
├── static/
│   ├── css/
│   │   └── style.css               # Clean academic operations stylesheet
│   └── js/
│       └── app.js                  # Dynamic UI, auto-resolve & scenario loader
├── templates/
│   └── index.html                  # Responsive operations dashboard
├── app.py                          # Flask web server & REST API
├── demo_cli.py                     # Terminal-based demo script
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # Documentation
```

---

## 🚀 Quickstart & Execution

### 1. Installation

Ensure Python 3.10+ is installed:

```bash
git clone https://github.com/shaurya212121/PDL_lab_project.git
cd PDL_lab_project
pip install -r requirements.txt
```

### 2. Run Terminal CLI Demo

Run the quick terminal verification script:
```bash
python demo_cli.py
```
Output:
```text
======================================================================
   CLASHAUDIT: WORKLOAD DISTRIBUTION & CONFLICT DETECTOR
   PDL Lab Mini Project Demonstration
======================================================================

[STEP 1] Running Analysis on Collision Scenario:
  * Total Sessions Analyzed : 8
  * Hard Conflicts Detected : 2
  * Soft Warnings Detected  : 0
  * Workload Balance Index  : 95.0%

[DETECTED CONFLICTS]:
  [Hard Conflict] Faculty Double-Booking: Dr. Rajesh Sharma (Monday 10:00 - 11:00)
    --> Dr. Rajesh Sharma is simultaneously assigned to 2 classes at 10:00 - 11:00 on Monday: CS301 (CSE-A) in LH-101 & CS301 (CSE-B) in LH-102.
  [Hard Conflict] Room Collision: LH-101 (Wednesday 11:00 - 12:00)
    --> LH-101 is double-booked on Wednesday at 11:00 - 12:00 by: Prof. Ananya Iyer [CS302] & Dr. Amit Verma [CS303].

[SMART AI RESOLUTION SUGGESTION]:
  -> REASSIGN_FACULTY: Prof. Ananya Iyer is free on Monday at 10:00 - 11:00 and currently has available capacity (1 / 16 hrs).
  -> CHANGE_ROOM: Move CS303 to vacant room LH-203 on Wednesday at 11:00 - 12:00.

----------------------------------------------------------------------
[STEP 2] Testing ML Workload Burnout Risk Classifier:
  Input Faculty Profile:
    - Designation    : Assistant Professor (AICTE Cap: 18 hrs)
    - Teaching Hours : 16 hrs
    - Lab Hours      : 8 hrs
    - Total Hours    : 27 hrs/week

  ML Prediction Result: Overloaded (High Burnout Risk)
  Confidence          : 99.77%
======================================================================
```

### 3. Launch Web Dashboard

```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in any web browser.

---

## 📡 REST API Endpoints

- `GET /` — Web Dashboard UI
- `GET /api/scenarios` — Returns preconfigured academic timetable scenarios
- `POST /api/analyze` — Analyzes schedule, identifies clashes, computes WBI, and returns substitution recommendations
- `POST /api/resolve` — Executes smart re-assignment to eliminate timetable collisions
- `POST /api/predict-stress` — Runs ML pipeline on faculty hours to predict burnout probability

---

## 📜 License

Created for the **Python Data Lab (PDL)** Mini Project.
