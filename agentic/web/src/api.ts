export async function startRun(plan: any) {
  const res = await fetch('/runs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(plan)
  })
  return await res.json()
}

export function wsRun(id: string): WebSocket {
  return new WebSocket(`ws://${location.host}/ws/runs/${id}`)
}
