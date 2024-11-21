# autodev/services/llm_service.py

import os
import openai
import logging

logger = logging.getLogger(__name__)

def call_llm(prompt, model='o1-mini', max_completion_tokens=32768):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    openai.api_key = api_key

    try:
        logger.debug(f"Sending prompt to LLM:\n{prompt}")
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=max_completion_tokens,
        )
        content = response.choices[0].message.content.strip()
        logger.debug(f"Received response from LLM:\n{content}")
        return content
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return ""
