'use client'

interface SuggestedQuestionsProps {
  questions: string[]
  onSelect: (question: string) => void
}

export default function SuggestedQuestions({
  questions,
  onSelect,
}: SuggestedQuestionsProps) {
  if (questions.length === 0) return null

  return (
    <div className="px-4 pb-2">
      <p className="text-xs text-gray-500 mb-2">Suggested questions:</p>
      <div className="flex flex-wrap gap-2">
        {questions.map((question, index) => (
          <button
            key={index}
            onClick={() => onSelect(question)}
            className="px-3 py-1.5 bg-primary-50 hover:bg-primary-100 text-primary-700 text-sm rounded-full transition-colors border border-primary-200"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  )
}
