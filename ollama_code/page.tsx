'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

type Message = {
  role: 'user' | 'assistant'
  content: string
}

export default function Home() {
  const [prompt, setPrompt] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setIsLoading(true)
    const newMessages = [...messages, { role: 'user', content: prompt }]
    setMessages(newMessages)
    setPrompt('')

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: newMessages }),
      })
      const data = await response.json()
      if (response.ok) {
        setMessages([...newMessages, { role: 'assistant', content: data.generated_text }])
      } else {
        setMessages([...newMessages, { role: 'assistant', content: `Error: ${data.error}` }])
      }
    } catch (error) {
      setMessages([...newMessages, { role: 'assistant', content: 'An error occurred while generating the response.' }])
    }
    setIsLoading(false)
  }

  return (
    <div className="container mx-auto p-4">
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>Gemma2 Text Generator</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 mb-4 max-h-[60vh] overflow-y-auto">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] p-3 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 text-black'
                  }`}
                >
                  {message.content}
                </div>
              </div>
            ))}
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your prompt here"
              className="w-full"
            />
            <Button type="submit" disabled={isLoading} className="w-full">
              {isLoading ? 'Generating...' : 'Send'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

