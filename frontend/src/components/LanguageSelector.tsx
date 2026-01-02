'use client'

import { useLanguage } from '@/hooks/useLanguage'
import { Check } from 'lucide-react'
import { useEffect, useRef } from 'react'

const LANGUAGES = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
  { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்' },
  { code: 'raj', name: 'Rajasthani', nativeName: 'राजस्थानी' },
]

interface LanguageSelectorProps {
  onClose: () => void
}

export default function LanguageSelector({ onClose }: LanguageSelectorProps) {
  const { language, setLanguage } = useLanguage()
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        onClose()
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [onClose])

  const handleSelect = (code: string) => {
    setLanguage(code)
    onClose()
  }

  return (
    <div
      ref={ref}
      className="absolute right-0 top-full mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-lg z-50"
    >
      <div className="p-2">
        <p className="text-xs text-gray-500 px-2 py-1 uppercase tracking-wide">
          Select Language
        </p>
        <div className="mt-1">
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              onClick={() => handleSelect(lang.code)}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-md text-sm transition-colors ${
                language === lang.code
                  ? 'bg-primary-50 text-primary-700'
                  : 'hover:bg-gray-50 text-gray-700'
              }`}
            >
              <span>
                {lang.nativeName}{' '}
                <span className="text-gray-400">({lang.name})</span>
              </span>
              {language === lang.code && (
                <Check className="w-4 h-4 text-primary-600" />
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
