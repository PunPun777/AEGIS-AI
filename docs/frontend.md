# Frontend Documentation

## Framework

React 19 single-page application built with Vite.

---

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx                  Router setup (BrowserRouter, single route)
│   ├── main.jsx                 React DOM render entrypoint
│   ├── pages/
│   │   └── Home.jsx             Page shell: header, hero section, footer
│   ├── components/
│   │   ├── MainInterface.jsx    Primary dashboard: text analysis + live news
│   │   ├── InputBox.jsx         Text input with validation and loading states
│   │   ├── ResultCard.jsx       Single-text classification result display
│   │   ├── ConfidenceIndicator.jsx  Reusable confidence percentage + progress bar
│   │   └── SeverityBadge.jsx    Reusable severity level badge with colored bar
│   ├── services/
│   │   └── api.js               Axios HTTP client
│   └── styles/
│       └── App.css              Global design system
├── index.html
├── package.json
└── vite.config.js
```

---

## Dependencies

| Package | Purpose |
|---|---|
| react | UI framework |
| react-dom | DOM rendering |
| react-router-dom | Client-side routing |
| axios | HTTP client for backend communication |

---

## Components

### App.jsx

Root component. Sets up `BrowserRouter` with a single route (`/` -> `Home`). Imports global styles.

### Home.jsx

Page-level layout component. Renders:

- **Header**: Logo, title ("AEGIS-AI"), subtitle, system status indicator
- **Hero section**: Page heading and description
- **MainInterface**: Primary interactive component
- **Footer**: Copyright line

### MainInterface.jsx

Core interactive component. Contains two columns:

**Left Column — Text Analysis:**
- `InputBox` for manual text input
- `ResultCard` for displaying the classification result, severity, and confidence
- Calls `POST /predict` via `predictText()`
- State holds the full prediction result object `{ prediction, confidence, severity }`

**Right Column — Live News Dashboard:**
- "Analyze Live News" button that calls `GET /news-analysis` via `fetchNewsAnalysis()`
- Loading state with spinner
- Region cards rendered from the response

**Region Card** (rendered per region):
- Region title
- Anomaly badge: red "Anomaly Detected" or green "Normal Activity"
- TES badge: color-coded (red > 0.7, orange >= 0.4, green < 0.4)
- Trend badge: red "increasing" with up arrow, green "decreasing" with down arrow, neutral "stable" with right arrow
- Event list: color-coded cards per article displaying prediction badge, headline, `SeverityBadge`, and `ConfidenceIndicator` side-by-side in a meta-wrapper

### InputBox.jsx

Controlled textarea component. Props:

| Prop | Type | Description |
|---|---|---|
| `value` | `string` | Current text value |
| `onChange` | `function` | Text change handler |
| `onSubmit` | `function` | Analyse button click handler |
| `loading` | `boolean` | Disables input and shows spinner |
| `error` | `string` | Error message to display |

### ResultCard.jsx

Displays the classification result for a single text input. Accepts `prediction`, `confidence`, and `severity` as props. Maps prediction labels to display metadata:

| Prediction | Icon | Label | Description |
|---|---|---|---|
| conflict | 🔴 | CONFLICT | High-risk geopolitical conflict activity detected |
| protest | 🟠 | PROTEST | Civil unrest or protest activity identified |
| normal | 🟢 | NORMAL | No significant threat indicators detected |

Renders `SeverityBadge` and `ConfidenceIndicator` side-by-side in a `result-card__meta-wrapper` at the card footer. The `severity` prop from the API response takes priority; `meta.severity` from the local `PREDICTION_META` map is the fallback when the prop is absent.

Props:

| Prop | Type | Description |
|---|---|---|
| `prediction` | `string` | Predicted class label |
| `confidence` | `float` | Model confidence score (0.0–1.0) |
| `severity` | `string` | Severity level from API: `"LOW"`, `"MEDIUM"`, `"HIGH"`, or `"CRITICAL"` |

### ConfidenceIndicator.jsx

Reusable component that visualizes model confidence as a labeled percentage and an animated progress bar.

**Props:**

| Prop | Type | Description |
|---|---|---|
| `confidence` | `float` | Model confidence score in range `[0.0, 1.0]` |

**Behavior:**

- Multiplies `confidence` by 100 and formats to two decimal places (e.g., `0.9642` → `"96.42%"`)
- Applies a CSS color class based on the confidence value:

| Range | Class | Color |
|---|---|---|
| >= 0.90 | `confidence--green` | Green (`#22c55e`) |
| >= 0.70 | `confidence--yellow` | Yellow (`#facc15`) |
| < 0.70 | `confidence--red` | Red (`#ef4444`) |

- Progress bar width is set via inline style to `${percentage}%`

### SeverityBadge.jsx

Reusable component that displays the event severity level as a label and a solid colored bar.

**Props:**

| Prop | Type | Description |
|---|---|---|
| `severity` | `string` | Severity level: `"LOW"`, `"MEDIUM"`, `"HIGH"`, or `"CRITICAL"` |

**Behavior:**

- Normalizes `severity` to lowercase to derive the CSS modifier class (e.g., `"CRITICAL"` → `severity--critical`)
- Falls back to `"LOW"` if `severity` is undefined or null
- Displays the severity label text and a solid colored bar, matching the style structure of `ConfidenceIndicator`:

| Severity | Class | Color |
|---|---|---|
| `LOW` | `severity--low` | Green (`#22c55e`) |
| `MEDIUM` | `severity--medium` | Yellow (`#facc15`) |
| `HIGH` | `severity--high` | Orange (`#f97316`) |
| `CRITICAL` | `severity--critical` | Red (`#ef4444`) |

- Used in both `ResultCard` (manual text analysis) and event cards in the live news dashboard
- Rendered in a flex meta-wrapper alongside `ConfidenceIndicator`; both components receive `flex: 1` to share space equally

---

## API Client

`services/api.js` creates an Axios instance with:

- Base URL: `http://127.0.0.1:8000`
- Content-Type: `application/json`

Exported functions:

| Function | Method | Endpoint | Response |
|---|---|---|---|
| `predictText(text)` | POST | `/predict` | `{ prediction, confidence, severity }` |
| `fetchNewsAnalysis()` | GET | `/news-analysis` | Region-grouped intelligence object |

---

## Design System

The frontend uses a dark glassmorphism theme defined in `styles/App.css`.

### Typography

- Primary: Inter (300–700)
- Monospace: JetBrains Mono (badges, labels, status text, confidence and severity values)

### Color Palette

| Token | Value | Usage |
|---|---|---|
| `--color-bg` | `#080c14` | Page background |
| `--color-surface` | `#0e1522` | Card backgrounds |
| `--color-accent` | `#2d7cf6` | Interactive elements |
| `--color-conflict` | `#ef4444` | Conflict indicators |
| `--color-protest` | `#f97316` | Protest indicators |
| `--color-normal` | `#22c55e` | Normal / safe indicators |

**Confidence color scale** (independent of prediction color):

| Confidence Range | Color |
|---|---|
| >= 90% | Green (`#22c55e`) |
| 70–89% | Yellow (`#facc15`) |
| < 70% | Red (`#ef4444`) |

**Severity color scale**:

| Severity | Color |
|---|---|
| LOW | Green (`#22c55e`) |
| MEDIUM | Yellow (`#facc15`) |
| HIGH | Orange (`#f97316`) |
| CRITICAL | Red (`#ef4444`) |

### Layout

- Responsive two-column layout (side-by-side above 768px, stacked below)
- Cards use glassmorphism: semi-transparent backgrounds, blur, subtle borders
- Badges use pill shapes with glow shadows matching their semantic color
- Meta section (severity + confidence) rendered in a flex row at the card footer with a subtle top border separator; each indicator receives equal width via `flex: 1`

---

## Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Development server: http://localhost:5173

Production build:

```bash
npm run build
npm run preview
```
