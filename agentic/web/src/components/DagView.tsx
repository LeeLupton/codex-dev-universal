import React from 'react'

export default function DagView({ steps }: { steps: any[] }) {
  return <pre>{JSON.stringify(steps, null, 2)}</pre>
}
