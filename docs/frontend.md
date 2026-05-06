# Frontend Documentation

## Framework

React 19 single-page application built with Vite.

---

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              Router setup (BrowserRouter, single route)
│   ├── main.jsx             React DOM render entrypoint
│   ├── pages/
│   │   └── Home.jsx         Page shell: header, hero section, footer
│   ├── components/
│   │   ├── MainInterface.jsx Primary dashboard: text analysis + live news
│   │   ├── InputBox.jsx      Text input with validation and loading states
│   │   └── ResultCard.jsx    Single-text classification result display
│   ├── services/
│   │   └── api.js            Axios HTTP client
│   └── styles/
│       └── App.css           Global design system
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

**Left Column -- Text Analysis:**
- `InputBox` for manual text input
- `ResultCard` for displaying the classification result
- Calls `POST /predict` via `predictText()`

**Right Column -- Live News Dashboard:**
- "Analyze Live News" button that calls `GET /news-analysis` via `fetchNewsAnalysis()`
- Loading state with spinner
- Region cards rendered from the response

**Region Card** (rendered per region):
- Region title
- Anomaly badge: red "Anomaly Detected" or green "Normal Activity"
- TES badge: color-coded (red > 0.7, orange >= 0.4, green < 0.4)
- Trend badge: red "increasing" with up arrow, green "decreasing" with down arrow, neutral "stable" with right arrow
- Event list: color-coded cards per article with prediction badge

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

Displays the classification result for a single text input. Maps prediction labels to display metadata:

| Prediction | Icon | Severity | Color |
|---|---|---|---|
| conflict | Red circle | CRITICAL | Red |
| protest | Orange circle | MODERATE | Orange |
| normal | Green circle | STABLE | Green |

Includes a decorative animated confidence bar.

---

## API Client

`services/api.js` creates an Axios instance with:

- Base URL: `http://127.0.0.1:8000`
- Content-Type: `application/json`

Exported functions:

| Function | Method | Endpoint |
|---|---|---|
| `predictText(text)` | POST | `/predict` |
| `fetchNewsAnalysis()` | GET | `/news-analysis` |

---

## Design System

The frontend uses a dark glassmorphism theme defined in `styles/App.css`.

### Typography

- Primary: Inter (300-700)
- Monospace: JetBrains Mono (badges, labels, status text)

### Color Palette

| Token | Value | Usage |
|---|---|---|
| `--color-bg` | `#080c14` | Page background |
| `--color-surface` | `#0e1522` | Card backgrounds |
| `--color-accent` | `#2d7cf6` | Interactive elements |
| `--color-conflict` | `#ef4444` | Conflict indicators |
| `--color-protest` | `#f97316` | Protest indicators |
| `--color-normal` | `#22c55e` | Normal/safe indicators |

### Layout

- Responsive two-column layout (side-by-side above 768px, stacked below)
- Cards use glassmorphism: semi-transparent backgrounds, blur, subtle borders
- Badges use pill shapes with glow shadows matching their semantic color

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
