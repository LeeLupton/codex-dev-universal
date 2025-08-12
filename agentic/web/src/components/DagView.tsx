import React from 'react'

export const DagView: React.FC<{ steps: any[] }> = ({ steps }) => {
  return (
    <ul>
      {steps.map((s) => (
        <li key={s.id}>{s.id} - {s.state}</li>
      ))}
    </ul>
  )
}
