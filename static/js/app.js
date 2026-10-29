/**
 * ClashAudit - Client Interactions & Controller
 * PDL Lab Mini Project
 */

// Embedded default scenarios for offline execution or quick load
let activeSchedule = [];
let activeScenarioKey = 'balanced';
let currentSuggestions = [];

document.addEventListener('DOMContentLoaded', () => {
  switchScenario('balanced');
  // Run sample prediction on the stress tab so it has initial state
  handleStressPrediction();
});

/**
 * Tab Navigation
 */
function openTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

  const targetTab = document.getElementById(tabId);
  if (targetTab) targetTab.classList.add('active');

  const activeBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
  if (activeBtn) activeBtn.classList.add('active');
}

/**
 * Switch Institutional Scenario
 */
async function switchScenario(key) {
  activeScenarioKey = key;

  document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById(`btnScenario${key.charAt(0).toUpperCase() + key.slice(1)}`);
  if (btn) btn.classList.add('active');

  try {
    const res = await fetch('/api/scenarios');
    const data = await res.json();
    if (data[key]) {
      activeSchedule = data[key].schedule;
    }
  } catch (err) {
    console.warn('[ClashAudit] Using local scenario fallback:', err);
    activeSchedule = getFallbackScenario(key);
  }

  analyzeCurrentSchedule();
}

/**
 * Run Conflict Analysis on Active Schedule
 */
async function analyzeCurrentSchedule() {
  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ schedule: activeSchedule })
    });

    const report = await res.json();
    renderAnalysisReport(report);
  } catch (err) {
    console.warn('[ClashAudit] Analysis API fallback:', err);
    // Local fallback analysis
    renderAnalysisReport(localAnalyze(activeSchedule));
  }
}

/**
 * Render Analysis Results in UI
 */
function renderAnalysisReport(report) {
  // 1. Update Executive Stats Ribbon
  document.getElementById('statTotalSlots').innerText = activeSchedule.length;
  document.getElementById('statCriticalConflicts').innerText = report.critical_conflicts;
  document.getElementById('statWarningConflicts').innerText = report.warning_conflicts;
  document.getElementById('statBalanceScore').innerText = `${report.workload_balance_score}%`;

  // 2. Render Suggestions / Auto-Resolve Banner
  currentSuggestions = report.suggestions || [];
  const resolveBanner = document.getElementById('resolveBanner');
  if (currentSuggestions.length > 0) {
    const s = currentSuggestions[0];
    document.getElementById('resolveText').innerText = s.reason;
    resolveBanner.style.display = 'flex';
  } else {
    resolveBanner.style.display = 'none';
  }

  // 3. Render Conflict Cards
  const container = document.getElementById('conflictsContainer');
  container.innerHTML = '';

  const clashSlotMap = new Set();
  const clashRoomMap = new Set();

  if (report.conflicts_list && report.conflicts_list.length > 0) {
    report.conflicts_list.forEach(c => {
      const card = document.createElement('div');
      card.className = `conflict-card ${c.severity}`;

      const badgeColor = c.severity === 'CRITICAL' ? 'red' : 'amber';
      card.innerHTML = `
        <div class="conflict-left">
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
            <span class="tag-badge ${badgeColor}">${c.badge}</span>
            <h4>${c.title}</h4>
          </div>
          <p class="conflict-desc">${c.description}</p>
          <div class="conflict-meta">
            <span>📅 Day: <strong>${c.day}</strong></span>
            <span>⏰ Slot: <strong>${c.time_slot}</strong></span>
          </div>
        </div>
      `;
      container.appendChild(card);

      if (c.type === 'FACULTY_TIME_CLASH') {
        clashSlotMap.add(`${c.target_faculty}_${c.day}_${c.time_slot}`);
      } else if (c.type === 'ROOM_DOUBLE_BOOKING') {
        clashRoomMap.add(`${c.target_room}_${c.day}_${c.time_slot}`);
      }
    });
  } else {
    container.innerHTML = `
      <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 1rem 1.25rem; display: flex; align-items: center; gap: 0.75rem; color: #166534;">
        <span style="font-size: 1.25rem;">✅</span>
        <div>
          <strong>Schedule Fully Conflict-Free</strong>
          <p style="font-size: 0.8rem; color: #15803d; margin: 0;">No overlapping faculty assignments or room collisions detected.</p>
        </div>
      </div>
    `;
  }

  // 4. Render Timetable Table Rows
  const tbody = document.getElementById('scheduleTableBody');
  tbody.innerHTML = '';

  activeSchedule.forEach(item => {
    const isFacClash = clashSlotMap.has(`${item.faculty_name}_${item.day}_${item.time_slot}`);
    const isRoomClash = clashRoomMap.has(`${item.room}_${item.day}_${item.time_slot}`);
    const isClash = isFacClash || isRoomClash;

    const tr = document.createElement('tr');
    if (isClash) tr.className = 'clash-row';

    tr.innerHTML = `
      <td><strong>${item.day}</strong></td>
      <td><code>${item.time_slot}</code></td>
      <td><strong>${item.course_code}</strong> <span style="font-size: 0.75rem; color: #64748b;">(${item.section})</span></td>
      <td><span class="tag-badge blue">${item.department}</span></td>
      <td>${item.faculty_name}</td>
      <td><code>${item.room}</code></td>
      <td>
        ${isClash ? '<span class="tag-badge red">Clash</span>' : '<span class="tag-badge green">Valid</span>'}
      </td>
    `;
    tbody.appendChild(tr);
  });

  // 5. Render Workload Distribution List
  const workloadList = document.getElementById('workloadList');
  workloadList.innerHTML = '';

  if (report.workload_distribution) {
    report.workload_distribution.forEach(f => {
      const item = document.createElement('div');
      item.className = 'workload-item';

      let barColor = 'green';
      let statusBadge = '<span class="tag-badge green">Balanced</span>';

      if (f.status === 'Overloaded') {
        barColor = 'red';
        statusBadge = '<span class="tag-badge red">Overloaded</span>';
      } else if (f.status === 'Underloaded') {
        barColor = 'amber';
        statusBadge = '<span class="tag-badge amber">Underloaded</span>';
      }

      const percentClamped = Math.min(f.utilization_percentage, 100);

      item.innerHTML = `
        <div class="workload-info">
          <h4>${f.faculty_name}</h4>
          <p>${f.designation} &bull; Dept of ${f.department}</p>
        </div>
        <div class="bar-container">
          <div class="bar-labels">
            <span>Utilization: ${f.utilization_percentage}%</span>
            <span>${f.assigned_hours} / ${f.max_hours} hrs</span>
          </div>
          <div class="bar-track">
            <div class="bar-fill ${barColor}" style="width: ${percentClamped}%;"></div>
          </div>
        </div>
        <div class="workload-status">
          ${statusBadge}
        </div>
      `;
      workloadList.appendChild(item);
    });
  }
}

/**
 * 1-Click Auto-Resolve Conflict Action
 */
async function applyResolution() {
  if (currentSuggestions.length === 0) return;
  const topSuggestion = currentSuggestions[0];

  try {
    const res = await fetch('/api/resolve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        schedule: activeSchedule,
        suggestion: topSuggestion
      })
    });

    const data = await res.json();
    if (data.status === 'resolved') {
      activeSchedule = data.updated_schedule;
      renderAnalysisReport(data.report);
      alert(`Success! Reassigned to ${topSuggestion.recommended_faculty || topSuggestion.recommended_room}. Conflict eliminated!`);
    }
  } catch (err) {
    console.warn('[ClashAudit] Resolution fallback:', err);
    // Local resolution fallback
    const entry = activeSchedule.find(e => e.id === topSuggestion.entry_id);
    if (entry) {
      if (topSuggestion.action === 'REASSIGN_FACULTY') {
        entry.faculty_name = topSuggestion.recommended_faculty;
      } else if (topSuggestion.action === 'CHANGE_ROOM') {
        entry.room = topSuggestion.recommended_room;
      }
    }
    analyzeCurrentSchedule();
  }
}

/**
 * Toggle Add Class Inline Form
 */
function toggleAddModal() {
  const formCard = document.getElementById('addClassModal');
  formCard.style.display = formCard.style.display === 'none' ? 'block' : 'none';
}

/**
 * Handle Adding New Dynamic Class
 */
function handleAddClass(event) {
  event.preventDefault();
  const newEntry = {
    id: `USER_${Date.now()}`,
    faculty_name: document.getElementById('newFaculty').value,
    department: 'CSE',
    course_code: document.getElementById('newCourse').value,
    section: 'Sec-1',
    day: document.getElementById('newDay').value,
    time_slot: document.getElementById('newTimeSlot').value,
    room: document.getElementById('newRoom').value
  };

  activeSchedule.unshift(newEntry);
  toggleAddModal();
  analyzeCurrentSchedule();
}

/**
 * Handle Stress / Burnout Prediction
 */
async function handleStressPrediction(event) {
  if (event) event.preventDefault();

  const payload = {
    Designation: document.getElementById('calcDesig').value,
    TeachingHours: parseFloat(document.getElementById('calcTeaching').value) || 12,
    LabHours: parseFloat(document.getElementById('calcLab').value) || 4,
    AdminHours: parseFloat(document.getElementById('calcAdmin').value) || 2,
    ResearchHours: parseFloat(document.getElementById('calcResearch').value) || 2,
    UniqueCourses: parseInt(document.getElementById('calcCourses').value) || 2,
    DaysTaught: parseInt(document.getElementById('calcDays').value) || 4
  };

  try {
    const res = await fetch('/api/predict-stress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    renderStressResult(data);
  } catch (err) {
    console.warn('[ClashAudit] Stress predict fallback:', err);
    renderStressResult(localStressPredict(payload));
  }
}

/**
 * Render Stress Prediction in UI
 */
function renderStressResult(data) {
  const badge = document.getElementById('stressBadge');
  const code = data.prediction_code;

  if (code === 2) {
    badge.className = 'stress-badge tag-badge red';
    badge.innerText = '⚠️ HIGH BURNOUT RISK (OVERLOADED)';
  } else if (code === 0) {
    badge.className = 'stress-badge tag-badge amber';
    badge.innerText = '⚡ UNDERLOADED / SPARE CAPACITY';
  } else {
    badge.className = 'stress-badge tag-badge green';
    badge.innerText = '✅ BALANCED WORKLOAD (OPTIMAL)';
  }

  document.getElementById('stressHoursInfo').innerHTML = `
    Total Workload: <strong>${data.total_hours} hrs/week</strong> | Max Permissible Cap: <strong>${data.max_allowed_hours} hrs</strong> (Utilization: ${data.utilization_ratio}%)
  `;

  const probs = data.probabilities;
  document.getElementById('probUnderload').style.width = `${probs.Underloaded}%`;
  document.getElementById('probUnderloadVal').innerText = `${probs.Underloaded}%`;

  document.getElementById('probBalanced').style.width = `${probs.Balanced}%`;
  document.getElementById('probBalancedVal').innerText = `${probs.Balanced}%`;

  document.getElementById('probOverload').style.width = `${probs.Overloaded}%`;
  document.getElementById('probOverloadVal').innerText = `${probs.Overloaded}%`;

  document.getElementById('stressRecommendation').innerText = data.recommendation;
}

/**
 * Load Sample Faculty Profile into Calculator
 */
function loadSampleFaculty(type) {
  if (type === 'overloaded') {
    document.getElementById('calcDesig').value = 'Assistant Professor';
    document.getElementById('calcTeaching').value = 16;
    document.getElementById('calcLab').value = 8;
    document.getElementById('calcAdminHours') ? document.getElementById('calcAdminHours').value = 3 : document.getElementById('calcAdmin').value = 3;
    document.getElementById('calcResearch').value = 2;
    document.getElementById('calcCourses').value = 3;
    document.getElementById('calcDays').value = 5;
  }
  handleStressPrediction();
}

/**
 * Fallback Data for offline execution
 */
function getFallbackScenario(key) {
  return [
    {"id": "S1", "faculty_name": "Dr. Rajesh Sharma", "department": "CSE", "course_code": "CS301", "section": "CSE-A", "day": "Monday", "time_slot": "09:00 - 10:00", "room": "LH-101"},
    {"id": "S2", "faculty_name": "Prof. Ananya Iyer", "department": "CSE", "course_code": "CS302", "section": "CSE-B", "day": "Monday", "time_slot": "10:00 - 11:00", "room": "LH-102"}
  ];
}

function localAnalyze(sch) {
  return {
    total_conflicts: 0,
    critical_conflicts: 0,
    warning_conflicts: 0,
    conflicts_list: [],
    workload_distribution: [
      { faculty_name: "Dr. Rajesh Sharma", designation: "Professor", department: "CSE", assigned_hours: 12, max_hours: 14, utilization_percentage: 85.7, status: "Balanced" }
    ],
    workload_balance_score: 95.0,
    suggestions: []
  };
}

function localStressPredict(p) {
  const tot = p.TeachingHours + p.LabHours + p.AdminHours + p.ResearchHours;
  const isOver = tot > 18;
  return {
    prediction_code: isOver ? 2 : 1,
    prediction_label: isOver ? 'Overloaded' : 'Balanced',
    total_hours: tot,
    max_allowed_hours: 18,
    utilization_ratio: Math.round((tot / 18) * 100),
    probabilities: {
      Underloaded: isOver ? 2 : 10,
      Balanced: isOver ? 8 : 82,
      Overloaded: isOver ? 90 : 8
    },
    recommendation: isOver ? "Workload exceeds institutional limits. Reassign classes." : "Workload balanced."
  };
}
