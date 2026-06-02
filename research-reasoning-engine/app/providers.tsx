'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactNode, useState } from 'react'

export function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        retry: 2,
        staleTime: 1000 * 60 * 3,
        refetchOnWindowFocus: false,
      },
    },
  }))

  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
}

