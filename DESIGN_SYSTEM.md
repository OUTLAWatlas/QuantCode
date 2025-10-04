# QuantCode Trading Platform Design System
*Version 1.0 | October 2025*

---

## Table of Contents
1. [Brand Identity](#brand-identity)
2. [Color Palette](#color-palette)
3. [Typography](#typography)
4. [Spacing & Grid System](#spacing--grid-system)
5. [UI Components](#ui-components)
6. [Visual Effects & Animations](#visual-effects--animations)
7. [Layout Guidelines](#layout-guidelines)
8. [Accessibility Standards](#accessibility-standards)
9. [Implementation Guidelines](#implementation-guidelines)

---

## Brand Identity

### Brand Personality
- **Professional & Trustworthy**: Clean, sophisticated design that instills confidence
- **Modern & Energetic**: Contemporary visual language that appeals to younger demographics
- **Data-Focused**: Clear hierarchy and presentation of financial information
- **Approachable**: User-friendly without compromising sophistication

---

## Color Palette

### Primary Colors

```css
/* Deep Navy - Primary Background */
--color-primary-dark: #1A1A2E;
/* RGB: 26, 26, 46 */
/* HSL: 240°, 28%, 14% */

/* Midnight Blue - Secondary Background */
--color-primary-medium: #16213E;
/* RGB: 22, 33, 62 */
/* HSL: 224°, 48%, 16% */

/* Royal Blue - Primary Accent */
--color-accent-primary: #0F3460;
/* RGB: 15, 52, 96 */
/* HSL: 213°, 73%, 22% */
```

### Status Colors

```css
/* Crimson Red - Negative/Error */
--color-negative: #E94560;
/* RGB: 233, 69, 96 */
/* HSL: 350°, 79%, 59% */

/* Emerald Green - Positive/Success */
--color-positive: #53BF9D;
/* RGB: 83, 191, 157 */
/* HSL: 161°, 46%, 54% */
```

### Neutral Colors

```css
/* Pure White - Text/Icons */
--color-text-primary: #FFFFFF;
/* RGB: 255, 255, 255 */

/* Text Variants */
--color-text-secondary: rgba(255, 255, 255, 0.8);
--color-text-tertiary: rgba(255, 255, 255, 0.6);
--color-text-disabled: rgba(255, 255, 255, 0.4);

/* Subtle Overlays */
--color-overlay-light: rgba(255, 255, 255, 0.1);
--color-overlay-medium: rgba(255, 255, 255, 0.2);
--color-overlay-dark: rgba(0, 0, 0, 0.3);
```

### Color Usage Guidelines

#### ✅ DO:
- Use `--color-primary-dark` for main backgrounds and navigation
- Use `--color-primary-medium` for card backgrounds and secondary surfaces
- Use `--color-accent-primary` exclusively for primary CTAs and active states
- Use status colors only for their intended purposes (positive/negative/error)
- Maintain consistent opacity levels for text hierarchy

#### ❌ DON'T:
- Mix accent colors for different UI elements
- Use status colors for decorative purposes
- Apply colors below 0.4 opacity for interactive elements
- Use colored backgrounds without sufficient contrast ratios

---

## Typography

### Font Families

```css
/* Headings Font */
--font-heading: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Body Text Font */
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Monospace Font (for financial data) */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
```

### Typography Scale

```css
/* Heading Sizes */
--text-h1: 2.5rem;      /* 40px - Page titles */
--text-h2: 2rem;        /* 32px - Section headers */
--text-h3: 1.5rem;      /* 24px - Subsection headers */
--text-h4: 1.25rem;     /* 20px - Card titles */
--text-h5: 1.125rem;    /* 18px - Small headers */

/* Body Text Sizes */
--text-body-large: 1.125rem;   /* 18px - Prominent text */
--text-body-base: 1rem;        /* 16px - Standard body text */
--text-body-small: 0.875rem;   /* 14px - Secondary text */
--text-caption: 0.75rem;       /* 12px - Captions, labels */

/* Financial Data Sizes */
--text-data-large: 1.5rem;     /* 24px - Major prices */
--text-data-base: 1.125rem;    /* 18px - Standard data */
--text-data-small: 1rem;       /* 16px - Minor data */
```

### Font Weights

```css
--weight-light: 300;
--weight-regular: 400;
--weight-medium: 500;
--weight-semibold: 600;
--weight-bold: 700;
```

### Line Heights

```css
--leading-tight: 1.2;     /* Headlines */
--leading-normal: 1.5;    /* Body text */
--leading-relaxed: 1.75;  /* Long-form content */
```

### Typography Usage

#### Headlines (Poppins)
```css
.heading-primary {
  font-family: var(--font-heading);
  font-size: var(--text-h1);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-tight);
  color: var(--color-text-primary);
}
```

#### Body Text (Inter)
```css
.text-body {
  font-family: var(--font-body);
  font-size: var(--text-body-base);
  font-weight: var(--weight-regular);
  line-height: var(--leading-normal);
  color: var(--color-text-primary);
}
```

#### Financial Data (Monospace)
```css
.text-financial {
  font-family: var(--font-mono);
  font-size: var(--text-data-base);
  font-weight: var(--weight-medium);
  line-height: var(--leading-normal);
  letter-spacing: 0.025em;
}
```

---

## Spacing & Grid System

### Spacing Scale

```css
/* Base spacing unit: 4px */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

### Grid System

```css
/* Container Widths */
--container-sm: 640px;
--container-md: 768px;
--container-lg: 1024px;
--container-xl: 1280px;
--container-2xl: 1536px;

/* Grid Columns */
--grid-cols-12: repeat(12, minmax(0, 1fr));
--grid-cols-6: repeat(6, minmax(0, 1fr));
--grid-cols-4: repeat(4, minmax(0, 1fr));
--grid-cols-3: repeat(3, minmax(0, 1fr));
--grid-cols-2: repeat(2, minmax(0, 1fr));

/* Gap Sizes */
--gap-sm: var(--space-4);    /* 16px */
--gap-md: var(--space-6);    /* 24px */
--gap-lg: var(--space-8);    /* 32px */
--gap-xl: var(--space-12);   /* 48px */
```

### Layout Examples

#### Main Container
```css
.container {
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: 0 var(--space-6);
}
```

#### Card Grid
```css
.card-grid {
  display: grid;
  grid-template-columns: var(--grid-cols-3);
  gap: var(--gap-md);
}

@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
```

---

## UI Components

### Buttons

#### Primary Button
```css
.btn-primary {
  /* Structure */
  padding: var(--space-3) var(--space-6);
  border: none;
  border-radius: 0; /* Sharp corners */
  cursor: pointer;
  
  /* Typography */
  font-family: var(--font-body);
  font-size: var(--text-body-base);
  font-weight: var(--weight-semibold);
  
  /* Colors */
  background: var(--color-accent-primary);
  color: var(--color-text-primary);
  
  /* Effects */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  box-shadow: 0 0 20px rgba(15, 52, 96, 0.4);
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}
```

#### Secondary Button
```css
.btn-secondary {
  padding: var(--space-3) var(--space-6);
  border: 2px solid var(--color-overlay-medium);
  border-radius: 0;
  background: transparent;
  color: var(--color-text-primary);
  font-family: var(--font-body);
  font-size: var(--text-body-base);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  border-color: var(--color-accent-primary);
  background: var(--color-overlay-light);
}
```

#### Button Sizing
```css
.btn-large {
  padding: var(--space-4) var(--space-8);
  font-size: var(--text-body-large);
}

.btn-small {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-body-small);
}
```

### Cards

#### Base Card
```css
.card {
  /* Structure */
  background: var(--color-primary-medium);
  border: 1px solid var(--color-overlay-light);
  border-radius: 8px;
  padding: var(--space-6);
  
  /* Frosted Glass Effect */
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  
  /* Shadow */
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  
  /* Transition */
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}
```

#### Status Cards
```css
.card-positive {
  border-left: 4px solid var(--color-positive);
}

.card-negative {
  border-left: 4px solid var(--color-negative);
}

.card-neutral {
  border-left: 4px solid var(--color-accent-primary);
}
```

### Form Elements

#### Input Fields
```css
.input-field {
  /* Container */
  position: relative;
  margin-bottom: var(--space-6);
}

.input-label {
  /* Label */
  display: block;
  font-family: var(--font-body);
  font-size: var(--text-body-small);
  font-weight: var(--weight-medium);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
}

.input {
  /* Structure */
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: var(--color-primary-dark);
  border: none;
  border-bottom: 2px solid var(--color-overlay-medium);
  
  /* Typography */
  font-family: var(--font-body);
  font-size: var(--text-body-base);
  color: var(--color-text-primary);
  
  /* Effects */
  transition: border-color 0.2s ease;
  outline: none;
}

.input:focus {
  border-bottom-color: var(--color-accent-primary);
}

.input::placeholder {
  color: var(--color-text-tertiary);
}
```

#### Select Dropdown
```css
.select {
  /* Structure */
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: var(--color-primary-medium);
  border: 1px solid var(--color-overlay-medium);
  border-radius: 4px;
  
  /* Typography */
  font-family: var(--font-body);
  font-size: var(--text-body-base);
  color: var(--color-text-primary);
  
  /* Effects */
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.select:focus {
  border-color: var(--color-accent-primary);
  outline: none;
}
```

### Navigation

#### Header Navigation
```css
.nav-header {
  background: var(--color-primary-dark);
  border-bottom: 1px solid var(--color-overlay-light);
  padding: var(--space-4) 0;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.nav-list {
  display: flex;
  gap: var(--space-8);
  align-items: center;
}

.nav-link {
  font-family: var(--font-body);
  font-size: var(--text-body-base);
  font-weight: var(--weight-medium);
  color: var(--color-text-secondary);
  text-decoration: none;
  padding: var(--space-2) var(--space-4);
  border-radius: 4px;
  transition: all 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  color: var(--color-text-primary);
  background: var(--color-overlay-light);
}
```

---

## Visual Effects & Animations

### Micro-interactions

#### Shimmer Effect
```css
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.shimmer {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.shimmer-trigger:hover .shimmer {
  animation-play-state: running;
}
```

#### Smooth Fade-in
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.4s ease-out;
}

.fade-in-delayed {
  animation: fadeIn 0.4s ease-out 0.2s both;
}
```

#### Primary Action Animation
```css
@keyframes pulseGlow {
  0% {
    box-shadow: 0 0 20px rgba(15, 52, 96, 0.4);
  }
  50% {
    box-shadow: 0 0 30px rgba(15, 52, 96, 0.8);
  }
  100% {
    box-shadow: 0 0 20px rgba(15, 52, 96, 0.4);
  }
}

.btn-primary.success {
  animation: pulseGlow 0.8s ease-in-out;
}
```

### Market Pulse Background

```css
@keyframes marketPulse {
  0%, 100% {
    opacity: 0.1;
    transform: scale(1);
  }
  50% {
    opacity: 0.3;
    transform: scale(1.02);
  }
}

.market-pulse-bullish {
  background: radial-gradient(
    circle at center,
    rgba(83, 191, 157, 0.1) 0%,
    transparent 70%
  );
  animation: marketPulse 4s ease-in-out infinite;
}

.market-pulse-bearish {
  background: radial-gradient(
    circle at center,
    rgba(233, 69, 96, 0.1) 0%,
    transparent 70%
  );
  animation: marketPulse 4s ease-in-out infinite;
}
```

### Loading States

```css
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-overlay-medium);
  border-top-color: var(--color-accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes skeleton {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-overlay-light) 25%,
    var(--color-overlay-medium) 50%,
    var(--color-overlay-light) 75%
  );
  background-size: 200% 100%;
  animation: skeleton 1.5s infinite;
  border-radius: 4px;
}
```

---

## Layout Guidelines

### Visual Hierarchy Principles

#### Size Hierarchy
1. **Primary CTA**: Largest interactive element (btn-large)
2. **Secondary Actions**: Medium size (btn-primary)
3. **Tertiary Actions**: Smallest size (btn-small)

#### Color Hierarchy
1. **Primary Action**: `--color-accent-primary` exclusively
2. **Status Indicators**: `--color-positive` / `--color-negative`
3. **Secondary Elements**: `--color-overlay-medium`

#### Spacing Hierarchy
```css
/* Around primary CTA */
.cta-container {
  padding: var(--space-16) var(--space-8);
}

/* Around secondary content */
.content-section {
  padding: var(--space-12) var(--space-6);
}

/* Around supporting elements */
.supporting-content {
  padding: var(--space-8) var(--space-4);
}
```

### Focus Mode Toggle

```css
.focus-mode-active {
  /* Hide non-essential elements */
}

.focus-mode-active .sidebar,
.focus-mode-active .secondary-nav,
.focus-mode-active .footer {
  display: none;
}

.focus-mode-active .main-content {
  max-width: 100%;
  padding: var(--space-8);
}

.focus-mode-toggle {
  position: fixed;
  top: var(--space-4);
  right: var(--space-4);
  z-index: 1000;
  background: var(--color-primary-medium);
  border: 1px solid var(--color-overlay-medium);
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.focus-mode-toggle:hover {
  background: var(--color-accent-primary);
}
```

---

## Accessibility Standards

### Color Contrast
- **Text on Dark Background**: Minimum 4.5:1 ratio
- **Large Text**: Minimum 3:1 ratio
- **Interactive Elements**: Minimum 3:1 ratio for borders

### Focus States
```css
.focusable:focus {
  outline: 2px solid var(--color-accent-primary);
  outline-offset: 2px;
}

.btn:focus {
  box-shadow: 0 0 0 3px rgba(15, 52, 96, 0.3);
}
```

### Motion Preferences
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  .market-pulse-bullish,
  .market-pulse-bearish {
    animation: none;
  }
}
```

---

## Implementation Guidelines

### CSS Custom Properties Setup

```css
:root {
  /* Import all design tokens */
  
  /* Colors */
  --color-primary-dark: #1A1A2E;
  --color-primary-medium: #16213E;
  --color-accent-primary: #0F3460;
  --color-negative: #E94560;
  --color-positive: #53BF9D;
  --color-text-primary: #FFFFFF;
  
  /* Typography */
  --font-heading: 'Poppins', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  /* ... all spacing values */
  
  /* Effects */
  --blur-sm: 4px;
  --blur-md: 8px;
  --blur-lg: 16px;
  
  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-normal: 0.2s ease;
  --transition-slow: 0.3s ease;
}
```

### Component Architecture

#### Base Components
1. **Buttons**: `btn-primary`, `btn-secondary`, `btn-danger`
2. **Cards**: `card`, `card-positive`, `card-negative`
3. **Forms**: `input`, `select`, `checkbox`, `radio`
4. **Navigation**: `nav-header`, `nav-sidebar`, `nav-tabs`

#### Utility Classes
```css
/* Spacing utilities */
.mt-4 { margin-top: var(--space-4); }
.mb-4 { margin-bottom: var(--space-4); }
.p-4 { padding: var(--space-4); }

/* Text utilities */
.text-primary { color: var(--color-text-primary); }
.text-secondary { color: var(--color-text-secondary); }
.text-positive { color: var(--color-positive); }
.text-negative { color: var(--color-negative); }

/* Display utilities */
.flex { display: flex; }
.grid { display: grid; }
.hidden { display: none; }
```

### Responsive Design

```css
/* Mobile First Approach */
.responsive-grid {
  display: grid;
  gap: var(--gap-sm);
  grid-template-columns: 1fr;
}

/* Tablet */
@media (min-width: 768px) {
  .responsive-grid {
    grid-template-columns: var(--grid-cols-2);
    gap: var(--gap-md);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .responsive-grid {
    grid-template-columns: var(--grid-cols-3);
    gap: var(--gap-lg);
  }
}

/* Large Desktop */
@media (min-width: 1280px) {
  .responsive-grid {
    grid-template-columns: var(--grid-cols-4);
    gap: var(--gap-xl);
  }
}
```

### Performance Guidelines

#### Critical CSS
- Load typography and color tokens first
- Inline critical above-the-fold styles
- Defer non-critical animations

#### Font Loading
```css
/* Optimal font loading */
@font-face {
  font-family: 'Poppins';
  src: url('/fonts/poppins-v20-latin-600.woff2') format('woff2');
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-v12-latin-regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

---

## Usage Do's and Don'ts

### ✅ DO:

#### Colors
- Use the exact hex values provided
- Maintain consistent opacity levels for text hierarchy
- Apply status colors only for their intended purposes
- Test color contrast ratios before implementation

#### Typography
- Use Poppins for headings and Inter for body text
- Maintain the established type scale
- Use appropriate font weights for hierarchy
- Implement proper line heights for readability

#### Spacing
- Follow the 4px base spacing unit
- Use consistent gap sizes for grid layouts
- Provide adequate white space around primary CTAs
- Maintain proportional spacing relationships

#### Components
- Apply hover states to all interactive elements
- Use appropriate component variants for different contexts
- Maintain consistent border radius values
- Implement proper focus states for accessibility

### ❌ DON'T:

#### Colors
- Don't use custom colors outside the defined palette
- Don't apply accent colors to multiple primary actions
- Don't use colors below 4.5:1 contrast ratio for text
- Don't mix warm and cool tones

#### Typography
- Don't use system fonts as primary choices
- Don't mix more than 3 font families
- Don't use font sizes outside the established scale
- Don't neglect proper font loading strategies

#### Spacing
- Don't use arbitrary spacing values
- Don't create cramped layouts without adequate breathing room
- Don't inconsistently apply spacing patterns
- Don't ignore responsive spacing adjustments

#### Components
- Don't create components without hover/focus states
- Don't use sharp corners on small interactive elements
- Don't neglect loading and error states
- Don't implement animations without reduced-motion preferences

---

## Version History

- **v1.0** (October 2025): Initial design system documentation
- **Future**: Component library integration, advanced animation patterns

---

*This design system is a living document. Updates should maintain backward compatibility and be communicated to all development teams.*