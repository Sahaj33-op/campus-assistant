'use client'

import { useState } from 'react'
import { MessageCircle, X, Minimize2 } from 'lucide-react'
import ChatInterface from './ChatInterface'

interface ChatWidgetProps {
  position?: 'bottom-right' | 'bottom-left'
  primaryColor?: string
}

export default function ChatWidget({
  position = 'bottom-right',
  primaryColor = '#2563eb',
}: ChatWidgetProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)

  const positionClasses =
    position === 'bottom-right' ? 'right-4 bottom-4' : 'left-4 bottom-4'

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className={`fixed ${positionClasses} z-50 w-14 h-14 rounded-full shadow-lg flex items-center justify-center transition-transform hover:scale-110`}
        style={{ backgroundColor: primaryColor }}
      >
        <MessageCircle className="w-6 h-6 text-white" />
      </button>
    )
  }

  return (
    <div
      className={`fixed ${positionClasses} z-50 ${
        isMinimized ? 'w-72' : 'w-96 h-[600px]'
      } flex flex-col bg-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden transition-all`}
    >
      {/* Header */}
      <div
        className="flex items-center justify-between px-4 py-3 text-white"
        style={{ backgroundColor: primaryColor }}
      >
        <div className="flex items-center gap-2">
          <MessageCircle className="w-5 h-5" />
          <span className="font-semibold">Campus Assistant</span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setIsMinimized(!isMinimized)}
            className="p-1 hover:bg-white/20 rounded transition-colors"
          >
            <Minimize2 className="w-4 h-4" />
          </button>
          <button
            onClick={() => setIsOpen(false)}
            className="p-1 hover:bg-white/20 rounded transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Chat Content */}
      {!isMinimized && (
        <div className="flex-1 overflow-hidden">
          <ChatInterface />
        </div>
      )}
    </div>
  )
}

// Export for embedding
export function initChatWidget(config?: {
  position?: 'bottom-right' | 'bottom-left'
  primaryColor?: string
}) {
  // This function can be called from external scripts to initialize the widget
  console.log('Chat widget initialized with config:', config)
}
