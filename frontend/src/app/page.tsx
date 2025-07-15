'use client'

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { toast } from "sonner"

export default function ChatPage() {
  const [query, setQuery] = useState("")
  const [messages, setMessages] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!query.trim()) return
    setMessages([...messages, `🧑 You: ${query}`, "🤖 Bot: "])
    setLoading(true)

    try {
      const response = await fetch('http://localhost:5000/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })

      if (!response.body) throw new Error("No stream")

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let result = ""
      const stream = new ReadableStream({
        async start(controller) {
          while (true) {
            const { done, value } = await reader.read()
            if (done) break
            const chunk = decoder.decode(value)
            result += chunk
            setMessages(prev => {
              const copy = [...prev]
              copy[copy.length - 1] = "🤖 Bot: " + result
              return copy
            })
          }
          controller.close()
          reader.releaseLock()
        }
      })

      await new Response(stream).text()
    } catch (err) {
      toast.error("Failed to get response")
      console.error(err)
    } finally {
      setLoading(false)
      setQuery("")
    }
  }

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-4">🧠 Mental Health Chatbot</h1>

      <div className="space-y-4">
        {messages.map((msg, i) => (
          <Card key={i}>
            <CardContent className="p-4 whitespace-pre-wrap">{msg}</CardContent>
          </Card>
        ))}
      </div>

      <div className="flex gap-2 mt-6">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about sleep, anxiety, stress..."
          className="flex-1"
        />
        <Button onClick={handleSend} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </Button>
      </div>
    </div>
  )
}
