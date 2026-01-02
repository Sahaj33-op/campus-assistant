'use client'

import { useState, useCallback } from 'react'
import { chatApi } from '@/lib/api'
import type { Message } from '@/lib/types'

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)

  const sendMessage = useCallback(
    async (content: string, language?: string) => {
      if (!content.trim()) return

      // Add user message immediately
      const userMessage: Message = {
        role: 'user',
        content: content.trim(),
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, userMessage])
      setIsLoading(true)
      setError(null)
      setSuggestions([])

      try {
        const response = await chatApi.sendMessage(
          content.trim(),
          sessionId || undefined,
          language
        )

        // Update session ID
        if (response.session_id) {
          setSessionId(response.session_id)
        }

        // Add assistant message
        const assistantMessage: Message = {
          role: 'assistant',
          content: response.response,
          timestamp: new Date(),
          detectedLanguage: response.detected_language,
          responseLanguage: response.response_language,
          intent: response.intent || undefined,
          confidence: response.confidence,
          sources: response.sources.map((s) => ({
            title: s.title,
            content: s.content,
            score: s.score,
          })),
          needsEscalation: response.needs_escalation,
        }
        setMessages((prev) => [...prev, assistantMessage])

        // Set suggested questions
        if (response.suggested_questions) {
          setSuggestions(response.suggested_questions)
        }
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Failed to send message'
        setError(errorMessage)

        // Add error message
        const errorResponse: Message = {
          role: 'assistant',
          content:
            "I'm sorry, I encountered an error. Please try again or contact the office for assistance.",
          timestamp: new Date(),
          needsEscalation: true,
        }
        setMessages((prev) => [...prev, errorResponse])
      } finally {
        setIsLoading(false)
      }
    },
    [sessionId]
  )

  const clearChat = useCallback(() => {
    setMessages([])
    setSessionId(null)
    setSuggestions([])
    setError(null)
  }, [])

  return {
    messages,
    isLoading,
    sendMessage,
    clearChat,
    suggestions,
    error,
    sessionId,
  }
}
