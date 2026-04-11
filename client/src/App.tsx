import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface p-6 font-sans">
      <div className="max-w-md w-full bg-surface-container-high rounded-xl p-8 border border-outline-variant/15 shadow-2xl">
        <h1 className="text-display-lg text-primary mb-2 -tracking-[-0.02em] font-bold">
          Stitch Tailwind setup
        </h1>
        <p className="text-on-surface-variant mb-6 text-[0.875rem]">
          The Cognitive Monolith Design System is active.
        </p>

        <button
          className="w-full bg-gradient-to-br from-primary to-primary-container text-surface-container-lowest font-medium rounded-md py-3 px-4 hover:opacity-90 transition-opacity"
          onClick={() => setCount((count) => count + 1)}
        >
          Count is {count}
        </button>
      </div>
    </div>
  )
}

export default App
