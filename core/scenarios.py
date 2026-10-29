"""
Predefined Timetable Scenarios for Instant Lab Demonstrations
"""

SCENARIOS = {
    "balanced": {
        "title": "Scenario A: Optimal & Balanced Timetable",
        "description": "Standard institutional schedule with zero collisions, distributed load across all designations, and balanced weekly quotas.",
        "schedule": [
            {"id": "S1", "faculty_name": "Dr. Rajesh Sharma", "department": "CSE", "course_code": "CS301", "course_name": "Operating Systems", "section": "CSE-A", "day": "Monday", "time_slot": "09:00 - 10:00", "room": "LH-101"},
            {"id": "S2", "faculty_name": "Prof. Ananya Iyer", "department": "CSE", "course_code": "CS302", "course_name": "Database Systems", "section": "CSE-B", "day": "Monday", "time_slot": "10:00 - 11:00", "room": "LH-102"},
            {"id": "S3", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS303", "course_name": "Computer Networks", "section": "CSE-A", "day": "Monday", "time_slot": "11:00 - 12:00", "room": "LH-101"},
            {"id": "S4", "faculty_name": "Dr. Priya Nair", "department": "CSE", "course_code": "CS304", "course_name": "Algorithms", "section": "CSE-B", "day": "Monday", "time_slot": "02:00 - 03:00", "room": "LH-103"},

            {"id": "S5", "faculty_name": "Dr. Rajesh Sharma", "department": "CSE", "course_code": "CS301", "course_name": "Operating Systems", "section": "CSE-A", "day": "Tuesday", "time_slot": "09:00 - 10:00", "room": "LH-101"},
            {"id": "S6", "faculty_name": "Prof. Ananya Iyer", "department": "CSE", "course_code": "CS302", "course_name": "Database Systems", "section": "CSE-B", "day": "Tuesday", "time_slot": "11:00 - 12:00", "room": "LH-102"},
            {"id": "S7", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS303", "course_name": "Computer Networks", "section": "CSE-A", "day": "Tuesday", "time_slot": "02:00 - 03:00", "room": "LH-101"},
            {"id": "S8", "faculty_name": "Dr. Suresh Patel", "department": "IT", "course_code": "IT301", "course_name": "Web Technologies", "section": "IT-A", "day": "Tuesday", "time_slot": "10:00 - 11:00", "room": "LH-201"},

            {"id": "S9", "faculty_name": "Prof. Sneha Deshmukh", "department": "IT", "course_code": "IT302", "course_name": "Cloud Computing", "section": "IT-A", "day": "Wednesday", "time_slot": "09:00 - 10:00", "room": "LH-201"},
            {"id": "S10", "faculty_name": "Dr. Vikram Gupta", "department": "AI-DS", "course_code": "AI301", "course_name": "Machine Learning", "section": "AI-A", "day": "Wednesday", "time_slot": "10:00 - 11:00", "room": "LH-301"},
            {"id": "S11", "faculty_name": "Dr. Pooja Menon", "department": "AI-DS", "course_code": "AI302", "course_name": "Deep Learning", "section": "AI-A", "day": "Wednesday", "time_slot": "11:00 - 12:00", "room": "LH-301"},
            {"id": "S12", "faculty_name": "Dr. Priya Nair", "department": "CSE", "course_code": "CS304", "course_name": "Algorithms", "section": "CSE-A", "day": "Wednesday", "time_slot": "02:00 - 03:00", "room": "LH-103"},

            {"id": "S13", "faculty_name": "Dr. Suresh Patel", "department": "IT", "course_code": "IT301", "course_name": "Web Technologies", "section": "IT-A", "day": "Thursday", "time_slot": "09:00 - 10:00", "room": "LH-201"},
            {"id": "S14", "faculty_name": "Dr. Vikram Gupta", "department": "AI-DS", "course_code": "AI301", "course_name": "Machine Learning", "section": "AI-A", "day": "Thursday", "time_slot": "11:00 - 12:00", "room": "LH-301"},
            {"id": "S15", "faculty_name": "Prof. Ananya Iyer", "department": "CSE", "course_code": "CS302", "course_name": "Database Systems", "section": "CSE-A", "day": "Thursday", "time_slot": "02:00 - 03:00", "room": "LH-102"},
            {"id": "S16", "faculty_name": "Dr. Pooja Menon", "department": "AI-DS", "course_code": "AI302", "course_name": "Deep Learning", "section": "AI-A", "day": "Thursday", "time_slot": "03:00 - 04:00", "room": "LH-301"}
        ]
    },

    "collision": {
        "title": "Scenario B: Critical Collisions (Faculty & Room Double-Booking)",
        "description": "Simulates real-world scheduling blunders: Dr. Rajesh Sharma double-booked on Monday 10:00-11:00, and Room LH-101 double-booked on Wednesday.",
        "schedule": [
            # Hard Clash 1: Dr. Rajesh Sharma assigned to two sections at same time
            {"id": "C1", "faculty_name": "Dr. Rajesh Sharma", "department": "CSE", "course_code": "CS301", "course_name": "Operating Systems", "section": "CSE-A", "day": "Monday", "time_slot": "10:00 - 11:00", "room": "LH-101"},
            {"id": "C2", "faculty_name": "Dr. Rajesh Sharma", "department": "CSE", "course_code": "CS301", "course_name": "Operating Systems", "section": "CSE-B", "day": "Monday", "time_slot": "10:00 - 11:00", "room": "LH-102"},

            # Hard Clash 2: Room LH-101 double-booked by two different faculty at same time
            {"id": "C3", "faculty_name": "Prof. Ananya Iyer", "department": "CSE", "course_code": "CS302", "course_name": "Database Systems", "section": "CSE-A", "day": "Wednesday", "time_slot": "11:00 - 12:00", "room": "LH-101"},
            {"id": "C4", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS303", "course_name": "Computer Networks", "section": "CSE-B", "day": "Wednesday", "time_slot": "11:00 - 12:00", "room": "LH-101"},

            # Standard slots
            {"id": "C5", "faculty_name": "Dr. Priya Nair", "department": "CSE", "course_code": "CS304", "course_name": "Algorithms", "section": "CSE-A", "day": "Tuesday", "time_slot": "09:00 - 10:00", "room": "LH-103"},
            {"id": "C6", "faculty_name": "Dr. Suresh Patel", "department": "IT", "course_code": "IT301", "course_name": "Web Technologies", "section": "IT-A", "day": "Tuesday", "time_slot": "11:00 - 12:00", "room": "LH-201"},
            {"id": "C7", "faculty_name": "Prof. Sneha Deshmukh", "department": "IT", "course_code": "IT302", "course_name": "Cloud Computing", "section": "IT-A", "day": "Thursday", "time_slot": "10:00 - 11:00", "room": "LH-201"},
            {"id": "C8", "faculty_name": "Dr. Vikram Gupta", "department": "AI-DS", "course_code": "AI301", "course_name": "Machine Learning", "section": "AI-A", "day": "Thursday", "time_slot": "02:00 - 03:00", "room": "LH-301"}
        ]
    },

    "overload": {
        "title": "Scenario C: Excessive Overload & Fatigue Clashes",
        "description": "Simulates disproportionate allocation: Junior faculty Dr. Amit Verma assigned 20+ hours, plus 4 back-to-back continuous lectures without rest on Tuesday.",
        "schedule": [
            # 4 consecutive hours on Tuesday for Dr. Priya Nair (Fatigue Warning)
            {"id": "O1", "faculty_name": "Dr. Priya Nair", "department": "CSE", "course_code": "CS304", "course_name": "Algorithms", "section": "CSE-A", "day": "Tuesday", "time_slot": "09:00 - 10:00", "room": "LH-103"},
            {"id": "O2", "faculty_name": "Dr. Priya Nair", "department": "CSE", "course_code": "CS304", "course_name": "Algorithms", "section": "CSE-B", "day": "Tuesday", "time_slot": "10:00 - 11:00", "room": "LH-103"},
            {"id": "O3", "faculty_name": "Dr. Priya Nair", "department": "CSE", "course_code": "CS305", "course_name": "Data Structures Lab", "section": "CSE-A", "day": "Tuesday", "time_slot": "11:00 - 12:00", "room": "Lab-1"},
            {"id": "O4", "faculty_name": "Dr. Priya Nair", "department": "CSE", "course_code": "CS305", "course_name": "Data Structures Lab", "section": "CSE-A", "day": "Tuesday", "time_slot": "12:00 - 01:00", "room": "Lab-1"},

            # Overload for Dr. Amit Verma (Total: 7 sessions scheduled here, exceeding standard proportion)
            {"id": "O5", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS303", "course_name": "Networks", "section": "CSE-A", "day": "Monday", "time_slot": "09:00 - 10:00", "room": "LH-101"},
            {"id": "O6", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS303", "course_name": "Networks", "section": "CSE-B", "day": "Monday", "time_slot": "11:00 - 12:00", "room": "LH-101"},
            {"id": "O7", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS303", "course_name": "Networks", "section": "CSE-A", "day": "Wednesday", "time_slot": "09:00 - 10:00", "room": "LH-101"},
            {"id": "O8", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS303", "course_name": "Networks", "section": "CSE-B", "day": "Wednesday", "time_slot": "02:00 - 03:00", "room": "LH-101"},
            {"id": "O9", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS306", "course_name": "Network Lab", "section": "CSE-A", "day": "Thursday", "time_slot": "09:00 - 10:00", "room": "Lab-2"},
            {"id": "O10", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS306", "course_name": "Network Lab", "section": "CSE-A", "day": "Thursday", "time_slot": "10:00 - 11:00", "room": "Lab-2"},
            {"id": "O11", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS306", "course_name": "Network Lab", "section": "CSE-B", "day": "Friday", "time_slot": "02:00 - 03:00", "room": "Lab-2"},
            {"id": "O12", "faculty_name": "Dr. Amit Verma", "department": "CSE", "course_code": "CS306", "course_name": "Network Lab", "section": "CSE-B", "day": "Friday", "time_slot": "03:00 - 04:00", "room": "Lab-2"},

            # Normal single classes
            {"id": "O13", "faculty_name": "Dr. Rajesh Sharma", "department": "CSE", "course_code": "CS301", "course_name": "Operating Systems", "section": "CSE-A", "day": "Monday", "time_slot": "02:00 - 03:00", "room": "LH-101"},
            {"id": "O14", "faculty_name": "Prof. Sneha Deshmukh", "department": "IT", "course_code": "IT302", "course_name": "Cloud Computing", "section": "IT-A", "day": "Wednesday", "time_slot": "10:00 - 11:00", "room": "LH-201"}
        ]
    }
}
