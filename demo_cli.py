"""
FacultySync AI - Terminal CLI Demonstration Script
Tests conflict detection, workload distribution, and ML burnout prediction from terminal.
"""

import os
import joblib
import pandas as pd
from core.conflict_detector import ConflictDetector
from core.scenarios import SCENARIOS

def main():
    print("=" * 70)
    print("   FACULTYSYNC AI: WORKLOAD DISTRIBUTION & CONFLICT DETECTOR")
    print("   PDL Lab Mini Project Demonstration")
    print("=" * 70)

    detector = ConflictDetector()

    # 1. Run Scenario B: Critical Collisions
    print("\n[STEP 1] Running Analysis on Collision Scenario:")
    collision_sched = SCENARIOS['collision']['schedule']
    report = detector.analyze_schedule(collision_sched)

    print(f"  * Total Sessions Analyzed : {len(collision_sched)}")
    print(f"  * Hard Conflicts Detected : {report['critical_conflicts']}")
    print(f"  * Soft Warnings Detected  : {report['warning_conflicts']}")
    print(f"  * Workload Balance Index  : {report['workload_balance_score']}%")

    print("\n[DETECTED CONFLICTS]:")
    for c in report['conflicts_list']:
        print(f"  [{c['badge']}] {c['title']} ({c['day']} {c['time_slot']})")
        print(f"    --> {c['description']}")

    if report['suggestions']:
        print("\n[SMART AI RESOLUTION SUGGESTION]:")
        for s in report['suggestions']:
            print(f"  -> {s['action']}: {s['reason']}")

    # 2. Test ML Burnout Predictor
    print("\n" + "-" * 70)
    print("[STEP 2] Testing ML Workload Burnout Risk Classifier:")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'model', 'workload_model.joblib')

    if os.path.exists(model_path):
        pipe = joblib.load(model_path)
        sample_faculty = pd.DataFrame([{
            'Designation': 'Assistant Professor',
            'TeachingHours': 16,
            'LabHours': 8,
            'AdminHours': 2,
            'ResearchHours': 1,
            'UniqueCourses': 3,
            'DaysTaught': 5
        }])

        pred = pipe.predict(sample_faculty)[0]
        probs = pipe.predict_proba(sample_faculty)[0]
        labels = ['Underloaded', 'Balanced', 'Overloaded (High Burnout Risk)']

        print("  Input Faculty Profile:")
        print("    - Designation    : Assistant Professor (AICTE Cap: 18 hrs)")
        print("    - Teaching Hours : 16 hrs")
        print("    - Lab Hours      : 8 hrs")
        print("    - Total Hours    : 27 hrs/week")
        print(f"\n  ML Prediction Result: {labels[pred]}")
        print(f"  Confidence          : {probs[pred]*100:.2f}%")
    else:
        print("  Model file not found. Run: python model/train.py")

    print("\n" + "=" * 70)
    print("To launch the Interactive Web Dashboard, run: python app.py")
    print("Then open: http://127.0.0.1:5000 in your browser.")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()
