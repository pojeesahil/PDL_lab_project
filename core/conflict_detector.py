"""
Faculty Workload Distribution & Conflict Detection Engine
PDL Lab Project - Practical Data Lab
"""

from collections import defaultdict
import numpy as np

# Standard time slots in sequence for consecutive hours checking
TIME_SLOTS = [
    "09:00 - 10:00",
    "10:00 - 11:00",
    "11:00 - 12:00",
    "12:00 - 01:00",
    "02:00 - 03:00",
    "03:00 - 04:00",
    "04:00 - 05:00"
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

DEFAULT_FACULTY_CATALOG = {
    "Dr. Rajesh Sharma": {"designation": "Professor", "department": "CSE", "max_hours": 14},
    "Prof. Ananya Iyer": {"designation": "Associate Professor", "department": "CSE", "max_hours": 16},
    "Dr. Amit Verma": {"designation": "Assistant Professor", "department": "CSE", "max_hours": 18},
    "Dr. Priya Nair": {"designation": "Assistant Professor", "department": "CSE", "max_hours": 18},
    "Dr. Suresh Patel": {"designation": "Associate Professor", "department": "IT", "max_hours": 16},
    "Prof. Sneha Deshmukh": {"designation": "Assistant Professor", "department": "IT", "max_hours": 18},
    "Dr. Vikram Gupta": {"designation": "Professor", "department": "AI-DS", "max_hours": 14},
    "Dr. Pooja Menon": {"designation": "Assistant Professor", "department": "AI-DS", "max_hours": 18}
}

class ConflictDetector:
    def __init__(self, faculty_catalog=None):
        self.catalog = faculty_catalog or DEFAULT_FACULTY_CATALOG

    def analyze_schedule(self, schedule_entries):
        """
        Analyze timetable schedule for collisions, fatigue, and workload distribution.
        """
        conflicts = []
        
        # 1. Check Faculty Time Collisions (Hard Conflict)
        faculty_slot_map = defaultdict(list)
        # 2. Check Room Double Booking (Hard Conflict)
        room_slot_map = defaultdict(list)
        # 3. Track Daily Hours and Slots per Faculty
        faculty_day_slots = defaultdict(lambda: defaultdict(list))
        # 4. Track Total Weekly Hours per Faculty
        faculty_total_hours = defaultdict(int)

        for entry in schedule_entries:
            f_name = entry.get('faculty_name')
            day = entry.get('day')
            slot = entry.get('time_slot')
            room = entry.get('room')
            
            faculty_slot_key = (f_name, day, slot)
            faculty_slot_map[faculty_slot_key].append(entry)

            room_slot_key = (room, day, slot)
            room_slot_map[room_slot_key].append(entry)

            faculty_day_slots[f_name][day].append(slot)
            faculty_total_hours[f_name] += 1

        # Evaluate Faculty Time Collisions
        for (f_name, day, slot), entries in faculty_slot_map.items():
            if len(entries) > 1:
                class_details = " & ".join([f"{e.get('course_code')} ({e.get('section')}) in {e.get('room')}" for e in entries])
                conflicts.append({
                    "id": f"CONF_FAC_{day}_{slot[:2]}",
                    "type": "FACULTY_TIME_CLASH",
                    "severity": "CRITICAL",
                    "badge": "Hard Conflict",
                    "title": f"Faculty Double-Booking: {f_name}",
                    "day": day,
                    "time_slot": slot,
                    "description": f"{f_name} is simultaneously assigned to {len(entries)} classes at {slot} on {day}: {class_details}.",
                    "involved_entries": [e.get('id') for e in entries],
                    "target_faculty": f_name
                })

        # Evaluate Room Double Booking
        for (room, day, slot), entries in room_slot_map.items():
            if len(entries) > 1:
                faculty_details = " & ".join([f"{e.get('faculty_name')} [{e.get('course_code')}]" for e in entries])
                conflicts.append({
                    "id": f"CONF_ROOM_{room}_{day}_{slot[:2]}",
                    "type": "ROOM_DOUBLE_BOOKING",
                    "severity": "CRITICAL",
                    "badge": "Hard Conflict",
                    "title": f"Room Collision: {room}",
                    "day": day,
                    "time_slot": slot,
                    "description": f"{room} is double-booked on {day} at {slot} by: {faculty_details}.",
                    "involved_entries": [e.get('id') for e in entries],
                    "target_room": room
                })

        # Evaluate Consecutive Hours & Daily Fatigue
        slot_index_map = {s: i for i, s in enumerate(TIME_SLOTS)}
        for f_name, day_dict in faculty_day_slots.items():
            for day, slots in day_dict.items():
                # Daily Hours cap check
                if len(slots) > 5:
                    conflicts.append({
                        "id": f"CONF_DAILY_{f_name}_{day}",
                        "type": "DAILY_LIMIT_EXCEEDED",
                        "severity": "WARNING",
                        "badge": "Soft Warning",
                        "title": f"Daily Teaching Cap Exceeded: {f_name}",
                        "day": day,
                        "time_slot": "Full Day",
                        "description": f"{f_name} has {len(slots)} teaching hours on {day}. Recommended daily maximum is 5 hours.",
                        "target_faculty": f_name
                    })

                # Consecutive hours check
                indices = sorted([slot_index_map[s] for s in slots if s in slot_index_map])
                streak = 1
                max_streak = 1
                for k in range(1, len(indices)):
                    if indices[k] == indices[k - 1] + 1:
                        streak += 1
                        max_streak = max(max_streak, streak)
                    else:
                        streak = 1

                if max_streak >= 4:
                    conflicts.append({
                        "id": f"CONF_FATIGUE_{f_name}_{day}",
                        "type": "CONSECUTIVE_FATIGUE",
                        "severity": "WARNING",
                        "badge": "Fatigue Warning",
                        "title": f"Consecutive Lecture Fatigue: {f_name}",
                        "day": day,
                        "time_slot": f"{max_streak} Hours Continuous",
                        "description": f"{f_name} has {max_streak} consecutive hours on {day} without a break.",
                        "target_faculty": f_name
                    })

        # Evaluate Weekly Quota Overload & Distribution
        workload_distribution = []
        hours_list = []

        all_faculty_names = set(list(self.catalog.keys()) + list(faculty_total_hours.keys()))
        for f_name in sorted(all_faculty_names):
            info = self.catalog.get(f_name, {"designation": "Assistant Professor", "department": "General", "max_hours": 16})
            assigned = faculty_total_hours.get(f_name, 0)
            max_h = info["max_hours"]
            hours_list.append(assigned)
            
            status = "Balanced"
            if assigned > max_h:
                status = "Overloaded"
                conflicts.append({
                    "id": f"CONF_OVERLOAD_{f_name}",
                    "type": "WEEKLY_OVERLOAD",
                    "severity": "WARNING",
                    "badge": "Overload Warning",
                    "title": f"Weekly Workload Exceeded: {f_name}",
                    "day": "Weekly Total",
                    "time_slot": f"{assigned} / {max_h} hrs",
                    "description": f"{f_name} ({info['designation']}) is assigned {assigned} hrs/week, exceeding AICTE limit of {max_h} hrs by {assigned - max_h} hrs.",
                    "target_faculty": f_name
                })
            elif assigned < (max_h * 0.65) and assigned > 0:
                status = "Underloaded"
            elif assigned == 0:
                status = "Unassigned"

            ratio = round((assigned / max_h) * 100, 1) if max_h else 0
            workload_distribution.append({
                "faculty_name": f_name,
                "designation": info["designation"],
                "department": info["department"],
                "assigned_hours": assigned,
                "max_hours": max_h,
                "utilization_percentage": ratio,
                "status": status
            })

        # Workload Balance Index (WBI): Standard deviation of hours
        wbi_score = 100.0
        if len(hours_list) > 1:
            std_dev = float(np.std(hours_list))
            # Standard deviation under 2 is well-balanced (100%), above 5 drops balance score
            wbi_score = round(max(0.0, min(100.0, 100.0 - (std_dev * 10))), 1)

        # Smart Auto-Reassignment Suggestions for Conflicting Entries
        suggestions = self._generate_suggestions(conflicts, schedule_entries, faculty_slot_map, faculty_total_hours)

        return {
            "total_conflicts": len(conflicts),
            "critical_conflicts": sum(1 for c in conflicts if c['severity'] == 'CRITICAL'),
            "warning_conflicts": sum(1 for c in conflicts if c['severity'] == 'WARNING'),
            "conflicts_list": conflicts,
            "workload_distribution": workload_distribution,
            "workload_balance_score": wbi_score,
            "suggestions": suggestions
        }

    def _generate_suggestions(self, conflicts, schedule_entries, faculty_slot_map, faculty_total_hours):
        """
        Generate smart substitution suggestions to resolve detected clashes.
        """
        suggestions = []
        entry_lookup = {e['id']: e for e in schedule_entries}

        for c in conflicts:
            if c['type'] == 'FACULTY_TIME_CLASH':
                involved = c.get('involved_entries', [])
                if len(involved) >= 2:
                    # Pick the second entry to suggest reassigning
                    clash_entry = entry_lookup.get(involved[1])
                    if clash_entry:
                        day = clash_entry['day']
                        slot = clash_entry['time_slot']
                        orig_fac = clash_entry['faculty_name']
                        dept = clash_entry.get('department', 'CSE')

                        # Search for eligible substitute faculty in same department
                        best_sub = None
                        min_load = 999
                        for f_name, f_info in self.catalog.items():
                            if f_name == orig_fac:
                                continue
                            if f_info['department'] != dept:
                                continue
                            
                            # Check if free at that slot
                            if len(faculty_slot_map.get((f_name, day, slot), [])) == 0:
                                current_load = faculty_total_hours.get(f_name, 0)
                                if current_load < f_info['max_hours'] and current_load < min_load:
                                    min_load = current_load
                                    best_sub = (f_name, f_info, current_load)

                        if best_sub:
                            suggestions.append({
                                "conflict_id": c['id'],
                                "entry_id": clash_entry['id'],
                                "action": "REASSIGN_FACULTY",
                                "course": f"{clash_entry['course_code']} ({clash_entry['section']})",
                                "current_faculty": orig_fac,
                                "recommended_faculty": best_sub[0],
                                "reason": f"{best_sub[0]} is free on {day} at {slot} and currently has available capacity ({best_sub[2]} / {best_sub[1]['max_hours']} hrs)."
                            })

            elif c['type'] == 'ROOM_DOUBLE_BOOKING':
                involved = c.get('involved_entries', [])
                if len(involved) >= 2:
                    clash_entry = entry_lookup.get(involved[1])
                    if clash_entry:
                        suggestions.append({
                            "conflict_id": c['id'],
                            "entry_id": clash_entry['id'],
                            "action": "CHANGE_ROOM",
                            "course": f"{clash_entry['course_code']} ({clash_entry['section']})",
                            "current_room": clash_entry['room'],
                            "recommended_room": "LH-203",
                            "reason": f"Move {clash_entry['course_code']} to vacant room LH-203 on {clash_entry['day']} at {clash_entry['time_slot']}."
                        })

        return suggestions
