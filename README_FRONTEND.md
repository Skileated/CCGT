# Frontend Overview

## Landing Page Overview

The landing page now features a modern hero section with a gradient background and smooth entrance animations. It includes:

- Hero headline and subheadline explaining CCGT
- Prominent CTA button ("Try Now") that smooth-scrolls to the user details form
- User Details Form (Name, Email optional, Organization optional), validated and stored locally (localStorage)
- Animated transition to the evaluation form

Classes and libraries:
- Tailwind classes for layout and spacing
- Framer Motion for fade-in and slide-up animations

Key code:
- `src/pages/Home.tsx` implements hero, details form, and evaluation form sections.

## Visualization Enhancements

### Node Graph
- Uses a perceptually uniform color map via `d3-scale-chromatic` (interpolateTurbo)
- Improved force simulation for smoother edge layout with collision handling
- Hover tooltips include sentence text, entropy, and node weight/importance
- Animated node entry and smoother link transitions

File: `src/components/GraphViz.tsx`

### Line Graph (New)
- A new line chart shows sentence-level coherence contribution
- X-axis: sentence index
- Y-axis: contribution (derived from node importance or 1 - entropy)
- Animated line drawing with grid and tooltips

File: `src/components/LineGraph.tsx`

Integrated in `src/pages/Dashboard.tsx` below the node graph.

## Usage
- Evaluate text from the Home page; after evaluation, the app navigates to Dashboard showing:
  - Result summary card
  - Coherence Node Graph
  - Sentence Contribution Line Graph
  - Disruption Report

## Backend Optimization Flag
- Backend supports an optional optimization toggle:
  - `backend/app/core/config.py`: `OPTIMIZED_MODE = True`
- This flag enables improved numerical stability and calibration on the backend without changing API contracts.

## Screenshots
- Hero + CTA + Form (add screenshots here)
- Node and Line graphs (add screenshots here)


