import React from "react";

/**
 * Manage Schedule Page
 *
 * Purpose:
 * - Allows users to view and manage schedules in a clean UI
 * - Fully theme-aware (uses CSS variables only)
 * - Responsive and reusable layout
 *
 * Notes:
 * - No hardcoded colors
 * - Styling relies on global theme variables
 * - Logic-free UI (as per issue scope)
 */

const ManageSchedule = () => {
  return (
    <div
      style={{
        padding: "1.5rem",
        backgroundColor: "var(--bg-primary)",
        color: "var(--text-primary)",
        minHeight: "100vh",
      }}
    >
      {/* Page Header */}
      <div style={{ marginBottom: "1.5rem" }}>
        <h1 style={{ fontSize: "1.6rem", fontWeight: "600" }}>
          Manage Schedule
        </h1>
        <p
          style={{
            color: "var(--text-secondary)",
            marginTop: "0.25rem",
            fontSize: "0.9rem",
          }}
        >
          View, organize, and manage schedules efficiently
        </p>
      </div>

      {/* Action Bar */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1rem",
          flexWrap: "wrap",
          gap: "0.75rem",
        }}
      >
        <span style={{ fontWeight: "500" }}>Current Schedule</span>

        <button
          style={{
            padding: "0.45rem 0.9rem",
            borderRadius: "6px",
            border: "1px solid var(--border-muted)",
            backgroundColor: "var(--accent)",
            color: "var(--accent-text)",
            cursor: "pointer",
          }}
        >
          Add Schedule
        </button>
      </div>

      {/* Schedule Table Container */}
      <div
        style={{
          border: "1px solid var(--border-muted)",
          borderRadius: "8px",
          overflowX: "auto",
          backgroundColor: "var(--bg-surface)",
        }}
      >
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            fontSize: "0.9rem",
          }}
        >
          <thead>
            <tr
              style={{
                backgroundColor: "var(--bg-muted)",
                textAlign: "left",
              }}
            >
              <th style={thStyle}>Day</th>
              <th style={thStyle}>Start Time</th>
              <th style={thStyle}>End Time</th>
              <th style={thStyle}>Status</th>
            </tr>
          </thead>

          <tbody>
            {scheduleData.map((item, index) => (
              <tr
                key={index}
                style={{
                  borderBottom: "1px solid var(--border-muted)",
                }}
              >
                <td style={tdStyle}>{item.day}</td>
                <td style={tdStyle}>{item.start}</td>
                <td style={tdStyle}>{item.end}</td>
                <td
                  style={{
                    ...tdStyle,
                    color:
                      item.status === "Active"
                        ? "var(--success)"
                        : "var(--warning)",
                    fontWeight: "500",
                  }}
                >
                  {item.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

/* -------------------- Reusable Styles -------------------- */

const thStyle = {
  padding: "0.75rem",
  fontWeight: "600",
  color: "var(--text-secondary)",
};

const tdStyle = {
  padding: "0.75rem",
};

/* -------------------- Temporary Mock Data -------------------- */
/* UI-only data (no backend interaction as per scope) */

const scheduleData = [
  { day: "Monday", start: "09:00 AM", end: "04:00 PM", status: "Active" },
  { day: "Tuesday", start: "10:00 AM", end: "05:00 PM", status: "Active" },
  { day: "Wednesday", start: "09:30 AM", end: "03:30 PM", status: "Inactive" },
  { day: "Thursday", start: "11:00 AM", end: "06:00 PM", status: "Active" },
  { day: "Friday", start: "09:00 AM", end: "02:00 PM", status: "Inactive" },
];

export default ManageSchedule;
