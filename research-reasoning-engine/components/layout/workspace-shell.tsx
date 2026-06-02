'use client'

import { ReactNode } from 'react'
import { AppSidebar } from '@/components/layout/app-sidebar'

export function WorkspaceShell({ children }: { children: ReactNode }) {
  return <div className="min-h-screen bg-[radial-gradient(circle_at_top,#1d4ed822,transparent_32%),#020617] text-slate-100"><div className="grid min-h-screen lg:grid-cols-[320px_1fr]"><div className="hidden lg:block"><AppSidebar /></div><main className="min-w-0 p-4 md:p-6 lg:p-8">{children}</main></div></div>
}

