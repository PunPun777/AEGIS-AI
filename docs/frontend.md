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
│   │   │   ├── ConfidenceIndicator.jsx  Reusable confidence percentage + progress bar
│   │   │   ├── intelligence/        Explainable Intelligence & TES UI
│   │   │   │   ├── ExplanationItem.jsx  Individual reasoning bullet
│   │   │   │   ├── ExplanationList.jsx  Container for reasoning items
│   │   │   │   ├── ExplanationPanel.jsx Collapsible reasoning UI component
│   │   │   │   ├── HybridDecisionPanel.jsx Collapsible UI for hybrid overrides
│   │   │   │   ├── RiskBadge.jsx        Risk level pill badge
│   │   │   │   ├── RiskMeter.jsx        Visual risk score fill bar
│   │   │   │   └── TESCard.jsx          Composite Threat Escalation Score card
│   │   │   ├── map/                 Geographic map components
│   │   │   │   ├── IntelligenceMap.jsx  Primary Leaflet map container
│   │   │   │   ├── RegionPopup.jsx      Interactive map marker popup
│   │   │   │   ├── RiskLegend.jsx       Color-coded map legend
│   │   │   │   └── MapControls.jsx      Fullscreen map controls
│   │   │   ├── EventCard.jsx        Reusable event card component
│   │   │   ├── SeverityBadge.jsx    Reusable severity level badge with colored bar
│   ├── services/
│   │   └── api.js               Axios HTTP client
│   └── styles/
│       ├── App.css              Global design system
│       └── map.css              Intelligence map styling
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
| leaflet | Core mapping library |
| react-leaflet | React bindings for Leaflet maps |

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

Core interactive component serving as the dashboard. Contains three primary sections:

**Top Section — Intelligence Map:**
- `IntelligenceMap`: Geographic visualization of regional risks, occupying the top portion of the dashboard.
- "Refresh Dashboard" button that simultaneously fetches map and news data.

**Bottom Left — Text Analysis:**
- `InputBox` for manual text input
- `ResultCard` for displaying the classification result, severity, and confidence
- Calls `POST /predict` via `predictText()`
- State holds the full prediction result object `{ prediction, confidence, severity, explanation }`

**Bottom Right — Live News Dashboard:**
- Region cards rendered from the `GET /news-analysis` response
- Displays detailed event breakdown for each region

**Region Card** (rendered per region):
- Region title
- Anomaly badge: red "Anomaly Detected" or green "Normal Activity"
- `TESCard`: rich composite card displaying the Threat Escalation Score, Risk Level badge, and visual Risk Meter
- Trend badge: red "increasing" with up arrow, green "decreasing" with down arrow, neutral "stable" with right arrow
- Event list: color-coded cards per article displaying prediction badge, headline, `SeverityBadge`, and `ConfidenceIndicator` side-by-side in a meta-wrapper, followed by the collapsible `ExplanationPanel` and `HybridDecisionPanel`.

### EventCard.jsx

Reusable presentation component for news events. Renders the prediction badge (with an additional "HYBRID OVERRIDE" badge if applicable), the headline, severity, confidence, and incorporates both the `ExplanationPanel` and `HybridDecisionPanel`.

### Map Components (components/map/)

- **`IntelligenceMap.jsx`**: The primary `react-leaflet` wrapper. Sets up the OpenStreetMap tile layer with custom dark-mode CSS filters. Iterates over regional intelligence data to render geographic circles at specific coordinates, colored by risk level.
- **`RegionPopup.jsx`**: An interactive Leaflet `<Popup>` containing a detailed breakdown of a region's intelligence payload (TES, Risk Level, Trend, Event Count, Average Confidence, and Severity Distribution).
- **`RiskLegend.jsx`**: A floating legend mapping the four risk levels to their respective colors.
- **`MapControls.jsx`**: Custom UI overlay for map actions (e.g., toggling fullscreen mode).

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

Renders the prediction badge (which dynamically says "HYBRID DECISION" or "ML PREDICTION"), `SeverityBadge`, and `ConfidenceIndicator` side-by-side in a `result-card__meta-wrapper` at the card footer, followed by the collapsible `ExplanationPanel` and `HybridDecisionPanel`.

Props:

| Prop | Type | Description |
|---|---|---|
| `result` | `object` | Full prediction result object containing prediction, confidence, severity, explanation, and hybrid override fields. |

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

### TESCard.jsx (and related)

Found in `components/intelligence/`, these components replace the legacy `TESBadge` with a richer intelligence card visualization.

- **`TESCard`**: The main composite component displaying the Threat Escalation Score, Risk Level (`RiskBadge`), and visual Risk Meter.
- **`RiskBadge`**: A pill-shaped badge component that accepts a `level` prop (`LOW`, `MODERATE`, `HIGH`, `CRITICAL`) and applies the appropriate color class dynamically.
- **`RiskMeter`**: A visual bar component that receives the `score` and `level` props. It calculates a fill percentage relative to the maximum TES value (`1.5`) and animates its width smoothly (`0.6s` cubic-bezier transition).

Used exclusively in the header section of region cards within the live news dashboard.

### ExplanationPanel.jsx & HybridDecisionPanel.jsx

Found in `components/intelligence/`, these components visualize the reasoning behind the model's prediction and the Hybrid Decision Engine's overrides.

- **`ExplanationPanel`**: A collapsible container with a smooth CSS Grid height transition. Toggles the visibility of the explanation list.
- **`ExplanationList`**: Maps an array of reasoning strings into individual items.
- **`ExplanationItem`**: Renders a single bullet point.
- **`HybridDecisionPanel`**: A collapsible container for hybrid overrides detailing the original ML prediction, the reasoning for the override, and lists of matched categories and keywords rendered as UI tags.

Renders gracefully underneath the meta-wrapper in both `ResultCard` and `EventCard`. Matches the dark glassmorphism aesthetic.

---

## API Client

`services/api.js` creates an Axios instance with:

- Base URL: `http://127.0.0.1:8000`
- Content-Type: `application/json`

Exported functions:

| Function | Method | Endpoint | Response |
|---|---|---|---|
| `predictText(text)` | POST | `/predict` | `{ prediction, confidence, severity, explanation }` |
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

**Risk Level color scale:**

| Risk Level | Score Range | Color |
|---|---|---|
| LOW | < 0.31 | Green (`#22c55e`) |
| MODERATE | 0.31–0.60 | Yellow (`#facc15`) |
| HIGH | 0.61–0.90 | Orange (`#f97316`) |
| CRITICAL | >= 0.91 | Red (`#ef4444`) |

### Layout

- Responsive two-column layout (side-by-side above 768px, stacked below)
- Cards use glassmorphism: semi-transparent backgrounds, blur, subtle borders
- Badges use pill shapes with glow shadows matching their semantic color
- `TESCard` uses a clean grid/flex layout containing the badge and meter elements, styled with dark glassmorphism.
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
