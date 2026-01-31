import os
import sys
from openai import OpenAI

def main():
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: No API key found (OPENROUTER_API_KEY or OPENAI_API_KEY)")
        sys.exit(1)
    
    print(f"API Key found: {api_key[:5]}...")
    
    # Configure client for OpenRouter
    base_url = "https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else None
    
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini" if base_url else "gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello"}],
        )
        print("Success! Response:", response.choices[0].message.content)
    except Exception as e:
        print(f"API Error: {e}")
        # Try finding available models if that fails?
        sys.exit(1)

if __name__ == "__main__":
    main()
