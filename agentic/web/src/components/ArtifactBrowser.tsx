import React from 'react'

export const ArtifactBrowser: React.FC<{ artifacts: any[] }> = ({ artifacts }) => (
  <ul>
    {artifacts.map(a => <li key={a.path}>{a.path}</li>)}
  </ul>
)
