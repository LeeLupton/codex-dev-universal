import React from 'react'

export default function ArtifactBrowser({ files }: { files: string[] }) {
  return (
    <ul>
      {files.map(f => <li key={f}>{f}</li>)}
    </ul>
  )
}
