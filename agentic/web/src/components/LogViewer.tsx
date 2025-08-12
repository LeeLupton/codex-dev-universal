import React from 'react'

export default function LogViewer({ logs }: { logs: string[] }) {
  return (
    <pre>{logs.join('\n')}</pre>
  )
}
