import { CopilotChat, CopilotKit } from '@copilotkit/react-core/v2'
import '@copilotkit/react-core/v2/styles.css'
import { bedrockAgent } from './agent'
import './App.css'

function App() {
  return (
    <CopilotKit selfManagedAgents={{ bedrock_assistant: bedrockAgent }}>
      <main className="app-shell">
        <header className="app-header">
          <div>
            <p className="eyebrow">React + CopilotKit + Strands Agents</p>
            <h1>Bedrock Assistant</h1>
          </div>
          <span className="status">AG-UI connected</span>
        </header>
        <section className="chat-panel" aria-label="Assistant chat">
          <CopilotChat agentId="bedrock_assistant" />
        </section>
      </main>
    </CopilotKit>
  )
}

export default App
