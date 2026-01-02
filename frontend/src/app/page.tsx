import ChatInterface from '@/components/ChatInterface'
import Header from '@/components/Header'

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <div className="flex-1 container mx-auto max-w-4xl px-4 py-6">
        <ChatInterface />
      </div>
    </main>
  )
}
