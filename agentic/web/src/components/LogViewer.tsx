import React from 'react'

export const LogViewer: React.FC<{ logs: string }> = ({ logs }) => (
  <pre>{logs}</pre>
)
