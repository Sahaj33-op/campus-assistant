'use client'

import { Bot, User, AlertCircle, ThumbsUp, ThumbsDown } from 'lucide-react'
import { useState } from 'react'
import type { Message } from '@/lib/types'

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const [feedback, setFeedback] = useState<'up' | 'down' | null>(null)
  const isUser = message.role === 'user'

  const handleFeedback = (type: 'up' | 'down') => {
    setFeedback(type)
    // TODO: Send feedback to API
  }

  return (
    <div
      className={`flex gap-3 animate-fadeInUp ${
        isUser ? 'flex-row-reverse' : ''
      }`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary-100 text-primary-600' : 'bg-gray-100 text-gray-600'
        }`}
      >
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      {/* Message Content */}
      <div className={`flex flex-col max-w-[75%] ${isUser ? 'items-end' : ''}`}>
        <div
          className={`px-4 py-3 rounded-2xl ${
            isUser
              ? 'bg-primary-600 text-white rounded-br-md'
              : 'bg-gray-100 text-gray-800 rounded-bl-md'
          }`}
        >
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>

        {/* Escalation Warning */}
        {message.needsEscalation && (
          <div className="flex items-center gap-2 mt-2 text-amber-600 text-sm">
            <AlertCircle className="w-4 h-4" />
            <span>For complex queries, please contact the office</span>
          </div>
        )}

        {/* Sources */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-2 text-xs text-gray-500">
            <span>Sources: </span>
            {message.sources.map((source, i) => (
              <span key={i} className="text-primary-600">
                {source.title}
                {i < message.sources!.length - 1 ? ', ' : ''}
              </span>
            ))}
          </div>
        )}

        {/* Confidence & Language */}
        {!isUser && message.confidence !== undefined && (
          <div className="flex items-center gap-3 mt-2 text-xs text-gray-400">
            <span>
              Confidence: {message.confidence}%
            </span>
            {message.detectedLanguage && (
              <span>Detected: {message.detectedLanguage}</span>
            )}
          </div>
        )}

        {/* Feedback buttons for assistant messages */}
        {!isUser && (
          <div className="flex items-center gap-2 mt-2">
            <button
              onClick={() => handleFeedback('up')}
              className={`p-1 rounded hover:bg-gray-200 transition-colors ${
                feedback === 'up' ? 'text-green-600' : 'text-gray-400'
              }`}
            >
              <ThumbsUp className="w-4 h-4" />
            </button>
            <button
              onClick={() => handleFeedback('down')}
              className={`p-1 rounded hover:bg-gray-200 transition-colors ${
                feedback === 'down' ? 'text-red-600' : 'text-gray-400'
              }`}
            >
              <ThumbsDown className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
