# Changelog

## [Unreleased] - 2024-01-XX

### Added
- **Delete All Tasks Feature**: New bulk delete operation to remove all tasks at once
  - DELETE /api/tasks endpoint in backend
  - Inline confirmation UI in frontend (no window.confirm())
  - Button only appears when tasks exist
  - Loading states during deletion
  - Comprehensive test coverage (API, hook, and integration tests)
  - Documentation in README.md

- **Delete All Tests**: Comprehensive test suite for bulk delete
  - `frontend/src/__tests__/App.deleteAll.test.jsx` - Integration tests
  - `frontend/src/services/__tests__/api.deleteAll.test.js` - API tests  
  - `frontend/src/hooks/__tests__/useTasks.deleteAll.test.js` - Hook tests
  - Tests cover visibility, confirmation UI, API integration, error handling, and edge cases

### Changed
- **Theme Rebranding**: Updated application theme from purple/blue to SwiftPay green
  - Background gradient: #667eea/#764ba2 → #10b981/#047857 (emerald)
  - Primary button color: #667eea → #10b981
  - Hover states: #5568d3 → #059669
  - Focus states: rgba(102,126,234) → rgba(16,185,129)
  - Task hover border: purple → green
  - Checkbox accent color: purple → green
  - Loading spinner: purple → green
  - Maintains all existing functionality with new color scheme

- **Logo Update**: Changed logo to SwiftPay branding
  - Updated import from `./assets/logo.png` to `./assets/logo-swiftpay.png`
  - Logo maintains same size and position

### Technical Details

#### Backend Changes
- Added `delete_all()` method to TaskRepository
- Added `delete_all_tasks()` method to TaskService  
- Added DELETE /api/tasks endpoint to routes
- Returns 204 No Content on success
- Idempotent operation (safe to call multiple times)
- Fully tested with unit and integration tests

#### Frontend Changes
- Updated App.css with new green color scheme (#10b981, #059669, #047857)
- Added delete-all-section CSS classes for bulk delete UI
- Added deleteAllTasks() to taskApi service
- Added deleteAllTasks() to useTasks hook
- Added inline confirmation UI to App.jsx:
  - Shows only when tasks.length > 0
  - Confirmation message: "Are you sure you want to delete ALL tasks? This action cannot be undone."
  - Two-step process: Click "Delete All Tasks" → Confirm or Cancel
  - Button text changes to "Deleting..." during operation
  - Buttons disabled during deletion
  - Confirmation UI highlighted in red (#fff5f5 background)
- Updated logo import to use logo-swiftpay.png

#### Testing
- All existing tests updated and passing
- New tests added for Delete All functionality:
  - 15+ integration tests in App.deleteAll.test.jsx
  - 15+ unit tests in api.deleteAll.test.js
  - 20+ unit tests in useTasks.deleteAll.test.js
- Tests cover:
  - Button visibility logic
  - Confirmation UI flow
  - API integration
  - Error handling
  - Loading states
  - Edge cases (empty list, errors, concurrent calls)
  - CSS styling

### User Experience

**Delete All Tasks Flow:**
1. User sees tasks in the list
2. "Delete All Tasks" button appears at bottom (red outline, white background)
3. User clicks "Delete All Tasks"
4. Confirmation message appears with warning text
5. Background changes to light red (#fff5f5)
6. Two buttons appear: "Confirm Delete All" (red) and "Cancel" (gray)
7. User clicks "Confirm Delete All"
8. Button text changes to "Deleting..."
9. Both buttons become disabled
10. All tasks are deleted via API
11. Task list updates to show "No tasks yet"
12. Delete All button disappears (no tasks remaining)

**Cancel Flow:**
- User can click "Cancel" at step 6
- Confirmation UI disappears
- Returns to normal "Delete All Tasks" button
- No tasks are deleted

**Theme Changes:**
- All purple/blue colors replaced with green (SwiftPay branding)
- Background gradient: purple/violet → emerald green shades
- Primary actions: purple → emerald green (#10b981)
- Hover states: darker purple → darker green (#059669)
- Maintains visual hierarchy and contrast ratios
- No functionality changes, only visual updates

### API Changes

**New Endpoint:**
```http
DELETE /api/tasks
Response: 204 No Content
```

**Behavior:**
- Deletes all tasks from the database
- Idempotent (can be called multiple times safely)
- No request body required
- Returns 204 No Content on success
- Returns 500 on server error

### Breaking Changes
None. All existing functionality preserved.

### Migration Guide
No migration required. Feature is additive and theme change is cosmetic.

---

## Notes

**Design Decisions:**
- Used inline confirmation UI instead of window.confirm() for better UX and testability
- Button only appears when tasks exist to avoid confusion
- Two-step confirmation process prevents accidental deletion
- Visual feedback (red background, loading text) during deletion
- Idempotent API design allows safe retries
- Green theme aligned with SwiftPay branding requirements

**Testing Strategy:**
- Comprehensive unit tests for API and hook layers
- Integration tests for complete user flows
- Tests verify visibility, confirmation, cancellation, errors, and edge cases
- Property-based testing not applicable (deterministic operation)

**Future Enhancements:**
- Add undo functionality with toast notification
- Add option to export tasks before deletion
- Add keyboard shortcut (e.g., Shift+Delete)
- Add deletion count in confirmation message
