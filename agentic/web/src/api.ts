export async function startRun(plan: any) {
  const res = await fetch('/runs', { method: 'POST', body: JSON.stringify(plan), headers: { 'Content-Type': 'application/json' } })
  return res.json()
}

export function wsRun(id: string): WebSocket {
  return new WebSocket(`ws://localhost:8080/ws/runs/${id}`)
}
