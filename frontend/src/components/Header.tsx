'use client'

import { GraduationCap, Globe } from 'lucide-react'
import { useState } from 'react'
import LanguageSelector from './LanguageSelector'

export default function Header() {
  const [showLanguages, setShowLanguages] = useState(false)

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto max-w-4xl px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-primary-600 text-white p-2 rounded-lg">
              <GraduationCap className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Campus Assistant</h1>
              <p className="text-sm text-gray-500">Multilingual AI Helpdesk</p>
            </div>
          </div>

          <div className="relative">
            <button
              onClick={() => setShowLanguages(!showLanguages)}
              className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Globe className="w-5 h-5" />
              <span className="text-sm">Language</span>
            </button>

            {showLanguages && (
              <LanguageSelector onClose={() => setShowLanguages(false)} />
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
