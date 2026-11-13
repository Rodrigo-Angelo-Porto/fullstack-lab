import { useState, useEffect } from 'react'
import { listEvents, register } from './api.js'

// Esta tela já tem a estrutura visual. Sua tarefa é ligá-la à API e ao estado React.
// Consulte docs/checkpoint-04.md antes de substituir os dados de exemplo.
export default function App() {
  const [userId, setUserId] = useState(1)
  const [events, setEvents] = useState([]) 
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [submittingId, setSubmittingId] = useState(null)
  const [message, setMessage] = useState(null)   

  useEffect(() => {
    listEvents()
      .then(data => setEvents(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleRegister(eventId) {
    setSubmittingId(eventId)
    setError(null)
    setMessage(null)
    try {
      await register(eventId, userId)
      setEvents(await listEvents())            
      setMessage('Inscrição realizada')
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmittingId(null)
    }
  }

  return <main className="page">
    <header>
      <p className="eyebrow">Trilha · Laboratório Full Stack</p>
      <h1>Eventos</h1>
      <p>Encontre uma atividade e garanta sua vaga.</p>
    </header>

    <label className="user-picker">Participante de demonstração
      <select value={userId} onChange={event => setUserId(Number(event.target.value))}>
        <option value="1">Pessoa 1</option>
        <option value="2">Pessoa 2</option>
      </select>
    </label>

    {error && <p role="alert">Não foi possível carregar os eventos: {error}</p>}
    {message && <p role="status">{message}</p>}

    <section aria-label="Lista de eventos" className="events">
    {loading && <p>Carregando eventos...</p>}
    {!loading && events.length === 0 && <p>Nenhum evento disponível.</p>}
    {events.map(event => (
      <article className="card" key={event.id}>
        <p className="date">{event.date}</p>
        <h2>{event.title}</h2>
        <p>
          {event.available_slots} {event.available_slots === 1 ? 'vaga disponível' : 'vagas disponíveis'}
        </p>
        <button
            type="button"
            disabled={submittingId === event.id || event.available_slots === 0}
            onClick={() => handleRegister(event.id)}
          >
          Inscrever-se
        </button>
      </article>
    ))}
  </section>
  </main>
}



