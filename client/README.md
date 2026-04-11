# Cognitive Monolith RAG Client

A modern, high-performance web interface for the Cognitive Monolith RAG (Retrieval-Augmented Generation) system. Built with React 19, Vite, Tailwind CSS v4, and Shadcn UI.

![Cognitive Monolith UI](https://raw.githubusercontent.com/shadcn.png) *Replace with actual app screenshot*

## ✨ Features

- **Midnight Design System**: A custom-crafted, dark-mode focused aesthetic using the "Obsidian/Midnight" color palette.
- **Responsive Layout**: Seamless transition between a powerful desktop sidebar-driven interface and a mobile-first bottom-nav experience.
- **Real-time Synthesis**: Beautifully styled intelligence output cards with citation support and status indicators.
- **Data Management**: Full visibility into your knowledge base corpus with file status tracking (INDEXED vs PENDING).
- **Advanced Querying**: A specialized footer interface for prompt engineering, including controls for temperature, max tokens, and model selection.
- **Visual Regression Testing**: Built-in Playwright suite for ensuring UI consistency across different viewports.

## 🚀 Tech Stack

- **Framework**: [React 19](https://react.dev/)
- **Build Tool**: [Vite 8](https://vite.dev/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **UI Components**: [Shadcn UI](https://ui.shadcn.com/) (Nova Preset)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Testing**: [Playwright](https://playwright.dev/)

## 🛠️ Development

### Prerequisites

- [pnpm](https://pnpm.io/) (v10 or higher recommended)
- Node.js (v20 or higher)

### Installation

```bash
cd client
pnpm install
```

### Running the App

```bash
pnpm dev
```
The app will be available at `http://localhost:5173`.

### Project Structure

- `src/components/ui`: Atomic Shadcn components.
- `src/components/layout`: Responsive shell (Sidebar, Header, MobileNav).
- `src/index.css`: Custom Tailwind v4 theme and "Midnight" design system variables.
- `src/App.tsx`: Main application assembly.

## 🧪 Testing

### Visual Regression Tests

We use Playwright to capture and verify the UI state:

```bash
# Run all tests
pnpm exec playwright test

# Run specifically the visual verification
pnpm exec playwright test tests/visual.spec.ts
```

Screenshots are saved in `tests/screenshots/` for review.

## 🎨 Design System

The project uses a custom Tailwind theme defined in `src/index.css`. Key colors include:

- **Background**: `#0b1326` (Midnight blue)
- **Primary**: `#c0c1ff` (Lavender)
- **Tertiary**: `#ffb783` (Peach/Orange)
- **Surface**: Multiple shades from `surface-container-low` to `highest` for depth.

---

*Part of the Cognitive Monolith RAG Ecosystem.*
