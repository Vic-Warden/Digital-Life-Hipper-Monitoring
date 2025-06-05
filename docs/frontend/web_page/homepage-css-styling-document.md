
# CSS Code Documentation

This documentation explains the purpose and design of each section in the CSS code for our Homepage, with references to color theory principles from Figma's guide.

---

##  Global Styles

```
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
```

**Purpose:** Ensures consistent box sizing and removes default spacing for all elements.

```
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #a8d8ff 0%, #b3e5fc 100%);
  min-height: 100vh;
  color: #333;
}
```

**Notes:**
- Uses a **cool gradient** (light blues) to evoke calm and clarity, inspired by analogous hues in the color wheel.
- Text color `#333` provides good contrast without being harsh black.

---

##  Header Layout

```
.header { ... }
.logo { ... }
.user-info { ... }
.settings-icon { ... }
```

**Purpose:** Creates a **frosted-glass header** using `backdrop-filter` and semi-transparent backgrounds. This gives a modern, airy aesthetic.

- `.settings-icon` includes a **hover animation** (rotation).
- `.user-profile` highlights interaction with hover movement.

---

##  Main Container and Card Layout

```
.container { ... }
.card { ... }
```

**Purpose:** Uses a **CSS Grid** layout to organize content into 3 columns (1 column on smaller screens).

- Cards have soft shadows, rounded corners, and blur effects to give a clean, elevated feel.
- Colors like `rgba(255, 255, 255, 0.95)` are used for semi-transparency while maintaining readability.

---

##  Mood + Activity Section

```
.mood-section { ... }
.mood-emoji { ... }
.activity-item { ... }
.activity-icon { ... }
```

**Color Theory Notes:**
- `.mood-emoji` uses **#ffd93d**, a **warm yellow** to express positivity and energy.
- Icons like `.steps-icon` (`#4caf50`, green) and `.time-icon` (`#2196f3`, blue) follow **analogous harmony** (green-blue palette) for cohesion.

- Includes subtle animations (`@keyframes bounce`) and transitions for interactivity.

---

##  Score Circle Section

```
.score-section { ... }
.score-fill { ... }
@keyframes fillProgress { ... }
```

**Functionality:**
- Displays a circular progress chart using a **conic gradient**.
- Green (`#4caf50`) indicates success, with soft background gray for contrast.
- Animation creates a **filling effect** to visually emphasize progress.

---

##  Goals Section

```
.goals-section { ... }
.goal-item { ... }
.progress-bar { ... }
.progress-fill { ... }
```

- Progress bars use a **green gradient** (`#4caf50` → `#8bc34a`) to represent growth and achievement.
- Streaks are marked with **red** (`#ff6b6b`) for attention and urgency.

---

##  Chart Section

```
.chart-section { ... }
.chart-container { ... }
.bar { ... }
.steps-bar, .pam-bar { ... }
```

- Uses bar charts to display metrics like steps and PAM.
- Color-coded bars:
  - **Blue** (`#2196f3`) for steps = trust, calm
  - **Green** (`#4caf50`) for PAM = balance, wellness
- Smooth transitions and value tooltips enhance usability.

---

##  Responsive Design

```
@media (max-width: 768px) { ... }
```

- Adjusts grid layout, header padding, and chart sizing for mobile screens.
- Ensures usability across devices with consistent visual quality.

---


## Reference link

[Colour Theory](https://www.figma.com/resource-library/what-is-color-theory/)