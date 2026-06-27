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
│   │   └── ConfidenceIndicator.jsx  Reusable confidence percentage + progress bar
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
- `ResultCard` for displaying the classification result and confidence
- Calls `POST /predict` via `predictText()`
- State holds the full prediction result object `{ prediction, confidence }`

**Right Column — Live News Dashboard:**
- "Analyze Live News" button that calls `GET /news-analysis` via `fetchNewsAnalysis()`
- Loading state with spinner
- Region cards rendered from the response

**Region Card** (rendered per region):
- Region title
- Anomaly badge: red "Anomaly Detected" or green "Normal Activity"
- TES badge: color-coded (red > 0.7, orange >= 0.4, green < 0.4)
- Trend badge: red "increasing" with up arrow, green "decreasing" with down arrow, neutral "stable" with right arrow
- Event list: color-coded cards per article, each displaying the prediction badge, headline, and a `ConfidenceIndicator`

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

Displays the classification result for a single text input. Accepts `prediction` and `confidence` as props. Maps prediction labels to display metadata:

| Prediction | Icon | Severity | Color |
|---|---|---|---|
| conflict | Red circle | CRITICAL | Red |
| protest | Orange circle | MODERATE | Orange |
| normal | Green circle | STABLE | Green |

Renders a `ConfidenceIndicator` in a visually separated footer section of the card.

Props:

| Prop | Type | Description |
|---|---|---|
| `prediction` | `string` | Predicted class label |
| `confidence` | `float` | Model confidence score (0.0–1.0) |

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

- The progress bar width is set via inline style to `${percentage}%`, driven directly by the confidence value
- Used in both `ResultCard` and individual event cards in the live news dashboard

---

## API Client

`services/api.js` creates an Axios instance with:

- Base URL: `http://127.0.0.1:8000`
- Content-Type: `application/json`

Exported functions:

| Function | Method | Endpoint | Response |
|---|---|---|---|
| `predictText(text)` | POST | `/predict` | `{ prediction, confidence }` |
| `fetchNewsAnalysis()` | GET | `/news-analysis` | Region-grouped intelligence object |

---

## Design System

The frontend uses a dark glassmorphism theme defined in `styles/App.css`.

### Typography

- Primary: Inter (300–700)
- Monospace: JetBrains Mono (badges, labels, status text, confidence values)

### Color Palette

| Token | Value | Usage |
|---|---|---|
| `--color-bg` | `#080c14` | Page background |
| `--color-surface` | `#0e1522` | Card backgrounds |
| `--color-accent` | `#2d7cf6` | Interactive elements |
| `--color-conflict` | `#ef4444` | Conflict indicators |
| `--color-protest` | `#f97316` | Protest indicators |
| `--color-normal` | `#22c55e` | Normal / safe indicators |

Confidence indicator uses its own color scale independent of the prediction color:

| Confidence Range | Color |
|---|---|
| >= 90% | Green (`#22c55e`) |
| 70–89% | Yellow (`#facc15`) |
| < 70% | Red (`#ef4444`) |

### Layout

- Responsive two-column layout (side-by-side above 768px, stacked below)
- Cards use glassmorphism: semi-transparent backgrounds, blur, subtle borders
- Badges use pill shapes with glow shadows matching their semantic color
- Confidence section rendered in a visually separated footer within each card, with a subtle top border

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
