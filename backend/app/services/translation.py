"""
Multilingual Translation Service.
Uses FREE translation libraries - NO API KEYS REQUIRED.
Supports 7+ Indian regional languages.
"""

import asyncio
from typing import Optional, Dict, Tuple
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
from loguru import logger

from app.core.config import get_settings, LANGUAGE_NAMES

settings = get_settings()


class TranslationService:
    """
    Handles language detection and translation.
    Uses deep-translator (free, no API key needed).
    Supports: English, Hindi, Gujarati, Marathi, Punjabi, Tamil, and more.
    """

    def __init__(self):
        # Language code mappings for deep-translator
        self.lang_codes = {
            "en": "en",
            "hi": "hi",
            "gu": "gu",
            "mr": "mr",
            "pa": "pa",
            "ta": "ta",
            "bn": "bn",
            "te": "te",
            "kn": "kn",
            "ml": "ml",
            "or": "or",
            "raj": "hi",  # Rajasthani uses Hindi as fallback
        }
        logger.info("Translation service initialized (using free Google Translate)")

    async def detect_language(self, text: str) -> str:
        """
        Detect the language of input text.
        Returns language code (en, hi, gu, etc.)
        """
        try:
            # Use langdetect for language detection
            detected = detect(text)

            # Map to our supported languages
            lang_mapping = {
                "en": "en",
                "hi": "hi",
                "gu": "gu",
                "mr": "mr",
                "pa": "pa",
                "ta": "ta",
                "bn": "bn",
                "te": "te",
                "kn": "kn",
                "ml": "ml",
                "or": "or",
            }

            lang = lang_mapping.get(detected, "en")
            logger.debug(f"Detected language: {detected} -> {lang}")
            return lang

        except LangDetectException:
            logger.warning("Could not detect language, defaulting to English")
            return "en"
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return "en"

    async def translate_to_english(self, text: str, source_lang: str) -> str:
        """
        Translate text from source language to English.
        Used for processing user queries.
        """
        if source_lang == "en":
            return text

        try:
            # Get the correct language code
            src_code = self.lang_codes.get(source_lang, source_lang)

            # Run translation in thread pool (deep_translator is synchronous)
            loop = asyncio.get_event_loop()
            translator = GoogleTranslator(source=src_code, target='en')
            translated = await loop.run_in_executor(
                None,
                translator.translate,
                text
            )

            logger.debug(f"Translated {source_lang} -> en: {text[:30]}... -> {translated[:30]}...")
            return translated

        except Exception as e:
            logger.warning(f"Translation failed ({source_lang} -> en): {e}")
            return text  # Return original if translation fails

    async def translate_from_english(self, text: str, target_lang: str) -> str:
        """
        Translate text from English to target language.
        Used for responding in user's preferred language.
        """
        if target_lang == "en":
            return text

        try:
            # Get the correct language code
            tgt_code = self.lang_codes.get(target_lang, target_lang)

            # Run translation in thread pool
            loop = asyncio.get_event_loop()
            translator = GoogleTranslator(source='en', target=tgt_code)
            translated = await loop.run_in_executor(
                None,
                translator.translate,
                text
            )

            logger.debug(f"Translated en -> {target_lang}")
            return translated

        except Exception as e:
            logger.warning(f"Translation failed (en -> {target_lang}): {e}")
            return text  # Return original if translation fails

    async def process_query(
        self, text: str, preferred_lang: Optional[str] = None
    ) -> Tuple[str, str, str]:
        """
        Process incoming query:
        1. Detect language
        2. Translate to English for processing
        3. Return (english_text, detected_lang, response_lang)
        """
        detected_lang = await self.detect_language(text)
        response_lang = preferred_lang or detected_lang

        if detected_lang == "en":
            return text, detected_lang, response_lang

        english_text = await self.translate_to_english(text, detected_lang)
        return english_text, detected_lang, response_lang

    async def prepare_response(
        self, english_response: str, target_lang: str
    ) -> str:
        """
        Prepare response in target language.
        """
        if target_lang == "en":
            return english_response

        return await self.translate_from_english(english_response, target_lang)

    def get_language_name(self, lang_code: str) -> str:
        """Get human-readable language name."""
        return LANGUAGE_NAMES.get(lang_code, "Unknown")

    def get_supported_languages(self) -> Dict[str, str]:
        """Get all supported languages."""
        return {
            code: LANGUAGE_NAMES[code]
            for code in settings.supported_languages
            if code in LANGUAGE_NAMES
        }


# Singleton instance
_translation_service: Optional[TranslationService] = None


def get_translation_service() -> TranslationService:
    """Get or create translation service instance."""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service
