import React, { useState } from 'react'
import { startRun } from '../api'

export default function WorkflowEditor() {
  const [text, setText] = useState('')
  const submit = async () => {
    await startRun(JSON.parse(text))
  }
  return (
    <div>
      <textarea value={text} onChange={e => setText(e.target.value)} />
      <button onClick={submit}>Validate</button>
    </div>
  )
}
