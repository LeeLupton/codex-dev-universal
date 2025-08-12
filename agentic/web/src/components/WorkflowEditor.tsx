import React, { useState } from 'react'

export const WorkflowEditor: React.FC = () => {
  const [text, setText] = useState('')
  return <textarea value={text} onChange={e => setText(e.target.value)} />
}
