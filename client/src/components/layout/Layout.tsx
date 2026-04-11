import React from "react"
import { Sidebar } from "./Sidebar"
import { MobileNav } from "./MobileNav"
import { Header } from "./Header"

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="flex min-h-screen bg-background text-foreground font-sans">
      {/* Sidebar - Desktop */}
      <Sidebar className="hidden lg:flex w-64 flex-col border-r border-border bg-surface-container-low" />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden pb-20 lg:pb-0">
        <Header />
        
        <main className="flex-1 overflow-auto p-4 lg:p-6">
          <div className="max-w-7xl mx-auto space-y-8">
            {children}
          </div>
        </main>
      </div>

      {/* Mobile Bottom Navigation */}
      <MobileNav className="lg:hidden fixed bottom-0 left-0 right-0 h-16 bg-surface-container-low border-t border-border z-50" />
    </div>
  )
}
