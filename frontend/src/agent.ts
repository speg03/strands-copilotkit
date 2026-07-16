import { HttpAgent } from '@ag-ui/client'

const agentUrl = import.meta.env.VITE_AGENT_URL ?? 'http://localhost:8000/'

export const bedrockAgent = new HttpAgent({ url: agentUrl })
