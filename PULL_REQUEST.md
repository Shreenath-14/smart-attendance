# Feature: Dynamic ML Service Health Check & Backend Fixes

## Summary

This PR replaces the hardcoded ML service status with a dynamic health check polling mechanism. It also resolves critical backend connection issues and frontend consistency bugs.

## Changes

### Frontend

- **Dynamic Polling:** Implemented `setInterval` in `Dashboard.jsx` and `MarkAttendance.jsx` to poll the ML service every 30 seconds.
- **Status Indicators:** Introduced logic to switch between 'checking' (Gray), 'ready' (Green), and 'waking-up' (Yellow) status badges based on service availability.
- **Timeout Handling:** Added a 10-second timeout to handle slow responses (typical of Render free tier) gracefully by showing a 'waking-up' state.
- **Linting & Code Cleanup:**
  - Removed unused variables (`navigate`, `status`, `snap`, etc.).
  - Fixed cascading render issues in `MarkAttendance.jsx` by refactoring state initialization.
  - Resolved CSS class conflicts in `Dashboard.jsx`.
  - Configured `axiosClient` and `.env` to correctly point to the backend at `http://localhost:8000`.

### Backend

- **MongoDB Connection:**
  - Updated `MONGO_URI` in `.env` to `mongodb://127.0.0.1:27017` to resolve IPv6 loopback issues (`WinError 10061`).
  - Added robust error handling in `main.py` startup to log warnings instead of crashing if the DB is unreachable.
  - Added `serverSelectionTimeoutMS` to `motor` client in `mongo.py` for faster failure feedback.
- **Configuration:** Unified config loading in `config.py` to correctly load the root `.env` via `pathlib`.
- **Debugging:** Added logging to authentication routes to trace login requests.
- **Dependencies:** Downgraded `bcrypt` to `4.0.1` to resolve `AttributeError`.

## Testing

- Verified ML service status updates in real-time.
- Confirmed Demo User creation (`teacher@gmail.com`) and login functionality.
- Validated MongoDB connection on local environment.
- Checked browser console for Health Check logs (`ML Status Check: 200`).

## Environment

- Requires `MONGO_URI` set to `mongodb://127.0.0.1:27017` locally.
- Requires `frontend/.env` with `VITE_API_URL=http://localhost:8000`.
