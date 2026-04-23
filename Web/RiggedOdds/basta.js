fetch('/api/play', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ luck: 1 })
})
.then(r => r.json())
.then(d => console.log(d.message));