'use client'

import { useState, useEffect, useCallback } from 'react'

const STORAGE_KEY = 'campus-assistant-language'
const DEFAULT_LANGUAGE = 'en'

export function useLanguage() {
  const [language, setLanguageState] = useState(DEFAULT_LANGUAGE)

  // Load from localStorage on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        setLanguageState(stored)
      }
    }
  }, [])

  const setLanguage = useCallback((lang: string) => {
    setLanguageState(lang)
    if (typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, lang)
    }
  }, [])

  return { language, setLanguage }
}
