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
│   │   ├── SeverityBadge.jsx    Reusable severity level badge with colored bar
│   │   └── TESBadge.jsx         Reusable TES score display with risk category label
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
- `TESBadge`: displays the weighted TES score and risk category label
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

Renders `SeverityBadge` and `ConfidenceIndicator` side-by-side in a `result-card__meta-wrapper` at the card footer.

Props:

| Prop | Type | Description |
|---|---|---|
| `prediction` | `string` | Predicted class label |
| `confidence` | `float` | Model confidence score (0.0–1.0) |
| `severity` | `string` | Severity level: `"LOW"`, `"MEDIUM"`, `"HIGH"`, or `"CRITICAL"` |

### ConfidenceIndicator.jsx

Reusable component that visualizes model confidence as a labeled percentage and an animated progress bar.

**Props:**

| Prop | Type | Description |
|---|---|---|
| `confidence` | `float` | Model confidence score in range `[0.0, 1.0]` |

**Color thresholds:**

| Range | Class | Color |
|---|---|---|
| >= 0.90 | `confidence--green` | Green (`#22c55e`) |
| >= 0.70 | `confidence--yellow` | Yellow (`#facc15`) |
| < 0.70 | `confidence--red` | Red (`#ef4444`) |

### SeverityBadge.jsx

Reusable component that displays the event severity level as a label and a solid colored bar.

**Props:**

| Prop | Type | Description |
|---|---|---|
| `severity` | `string` | Severity level: `"LOW"`, `"MEDIUM"`, `"HIGH"`, or `"CRITICAL"` |

**Color mapping:**

| Severity | Class | Color |
|---|---|---|
| `LOW` | `severity--low` | Green (`#22c55e`) |
| `MEDIUM` | `severity--medium` | Yellow (`#facc15`) |
| `HIGH` | `severity--high` | Orange (`#f97316`) |
| `CRITICAL` | `severity--critical` | Red (`#ef4444`) |

### TESBadge.jsx

Reusable component that displays the Threat Escalation Score alongside a derived risk category label.

**Props:**

| Prop | Type | Description |
|---|---|---|
| `tesScore` | `float` | Weighted TES value in range `[0.0, 1.5]` |

**Behavior:**

- Formats `tesScore` to two decimal places (e.g., `1.2164` → `"1.22"`)
- Derives `riskCategory` and `colorClass` from threshold comparisons:

| TES Range | Risk Category | Class | Color |
|---|---|---|---|
| >= 1.0 | Critical | `tes--critical` | Red (`#ef4444`) |
| >= 0.7 | High | `tes--high` | Orange (`#f97316`) |
| >= 0.4 | Moderate | `tes--moderate` | Yellow (`#facc15`) |
| < 0.4 | Low | `tes--low` | Green (`#22c55e`) |

- Renders a stacked layout: the pill badge (TES label + numeric score) stacked above the risk category text ("Critical Risk", "High Risk", etc.)
- Used exclusively in region cards within the live news dashboard
- Replaces the previous hardcoded inline TES conditional rendering in `MainInterface.jsx`

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
- Monospace: JetBrains Mono (badges, labels, status text, numeric values)

### Color Palette

| Token | Value | Usage |
|---|---|---|
| `--color-bg` | `#080c14` | Page background |
| `--color-surface` | `#0e1522` | Card backgrounds |
| `--color-accent` | `#2d7cf6` | Interactive elements |
| `--color-conflict` | `#ef4444` | Conflict indicators |
| `--color-protest` | `#f97316` | Protest indicators |
| `--color-normal` | `#22c55e` | Normal / safe indicators |

**Confidence color scale:**

| Confidence Range | Color |
|---|---|
| >= 90% | Green (`#22c55e`) |
| 70–89% | Yellow (`#facc15`) |
| < 70% | Red (`#ef4444`) |

**Severity color scale:**

| Severity | Color |
|---|---|
| LOW | Green (`#22c55e`) |
| MEDIUM | Yellow (`#facc15`) |
| HIGH | Orange (`#f97316`) |
| CRITICAL | Red (`#ef4444`) |

**TES risk category color scale:**

| Risk Category | TES Range | Color |
|---|---|---|
| Low | < 0.4 | Green (`#22c55e`) |
| Moderate | 0.4–0.69 | Yellow (`#facc15`) |
| High | 0.7–0.99 | Orange (`#f97316`) |
| Critical | >= 1.0 | Red (`#ef4444`) |

### Layout

- Responsive two-column layout (side-by-side above 768px, stacked below)
- Cards use glassmorphism: semi-transparent backgrounds, blur, subtle borders
- Badges use pill shapes with glow shadows matching their semantic color
- `TESBadge` uses a column layout: score pill on top, risk category text below, both sharing the same color via CSS descendant selectors on the indicator wrapper class
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
