"""
ClashAudit - Faculty Workload Distribution & Conflict Detector
PDL Lab Project - Practical Data Lab
"""

import os
import json
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
from core.conflict_detector import ConflictDetector, DEFAULT_FACULTY_CATALOG
from core.scenarios import SCENARIOS

app = Flask(__name__, static_folder='static', template_folder='templates')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'workload_model.joblib')
METADATA_PATH = os.path.join(BASE_DIR, 'model', 'model_metadata.json')

# Load trained ML model & metadata
ml_pipeline = None
model_meta = {}

try:
    if os.path.exists(MODEL_PATH):
        ml_pipeline = joblib.load(MODEL_PATH)
        print("[INFO] Workload ML Pipeline loaded successfully.")
    else:
        print("[WARNING] Model not found. Run model/train.py first.")
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")

try:
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r', encoding='utf-8') as f:
            model_meta = json.load(f)
        print("[INFO] Model metadata loaded successfully.")
except Exception as e:
    print(f"[ERROR] Failed to load metadata: {e}")

detector = ConflictDetector()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'ml_model_loaded': ml_pipeline is not None,
        'version': '1.0.0'
    })

@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    return jsonify({
        k: {
            "title": v["title"],
            "description": v["description"],
            "schedule": v["schedule"]
        } for k, v in SCENARIOS.items()
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json(force=True, silent=True)
    if not data or 'schedule' not in data:
        return jsonify({'error': 'Missing schedule entries in payload.'}), 400

    schedule = data['schedule']
    report = detector.analyze_schedule(schedule)
    return jsonify(report)

@app.route('/api/resolve', methods=['POST'])
def resolve():
    data = request.get_json(force=True, silent=True)
    if not data or 'schedule' not in data or 'suggestion' not in data:
        return jsonify({'error': 'Missing schedule or suggestion.'}), 400

    schedule = data['schedule']
    suggestion = data['suggestion']
    entry_id = suggestion.get('entry_id')
    action = suggestion.get('action')

    updated_schedule = []
    for entry in schedule:
        new_entry = dict(entry)
        if entry.get('id') == entry_id:
            if action == 'REASSIGN_FACULTY':
                new_entry['faculty_name'] = suggestion.get('recommended_faculty')
            elif action == 'CHANGE_ROOM':
                new_entry['room'] = suggestion.get('recommended_room')
        updated_schedule.append(new_entry)

    # Re-analyze updated schedule
    report = detector.analyze_schedule(updated_schedule)
    return jsonify({
        'status': 'resolved',
        'updated_schedule': updated_schedule,
        'report': report
    })

@app.route('/api/predict-stress', methods=['POST'])
def predict_stress():
    if ml_pipeline is None:
        return jsonify({'error': 'ML model not initialized. Please run model/train.py.'}), 500

    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'error': 'Missing payload.'}), 400

    try:
        desig = str(data.get('Designation', 'Assistant Professor'))
        teaching = float(data.get('TeachingHours', 12))
        lab = float(data.get('LabHours', 4))
        admin = float(data.get('AdminHours', 2))
        research = float(data.get('ResearchHours', 2))
        unique_courses = int(data.get('UniqueCourses', 2))
        days = int(data.get('DaysTaught', 4))

        input_df = pd.DataFrame([{
            'Designation': desig,
            'TeachingHours': teaching,
            'LabHours': lab,
            'AdminHours': admin,
            'ResearchHours': research,
            'UniqueCourses': unique_courses,
            'DaysTaught': days
        }])

        pred_class = int(ml_pipeline.predict(input_df)[0])
        probabilities = ml_pipeline.predict_proba(input_df)[0].tolist()

        class_labels = ['Underloaded', 'Balanced / Optimal', 'Overloaded (Burnout Risk)']
        label = class_labels[pred_class]

        total_hours = teaching + lab + admin + research
        max_h = 18 if desig == 'Assistant Professor' else 16 if desig == 'Associate Professor' else 14
        ratio = round((total_hours / max_h) * 100, 1)

        recommendation = ""
        if pred_class == 2:
            recommendation = f"Workload exceeds institutional limits ({total_hours:.0f}/{max_h} hrs). Reassign at least {total_hours - max_h:.0f} lecture/lab hours to adjunct or junior faculty."
        elif pred_class == 0:
            recommendation = f"Faculty is currently underutilized ({total_hours:.0f}/{max_h} hrs). Eligible to receive additional tutorial or lab mentoring duties."
        else:
            recommendation = f"Workload is well-balanced ({total_hours:.0f}/{max_h} hrs) in compliance with AICTE/UGC academic mandates."

        return jsonify({
            'prediction_code': pred_class,
            'prediction_label': label,
            'total_hours': total_hours,
            'max_allowed_hours': max_h,
            'utilization_ratio': ratio,
            'probabilities': {
                'Underloaded': round(probabilities[0] * 100, 1),
                'Balanced': round(probabilities[1] * 100, 1),
                'Overloaded': round(probabilities[2] * 100, 1)
            },
            'recommendation': recommendation
        })

    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    return jsonify(model_meta)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[*] Starting ClashAudit on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
