import os
from dotenv import load_dotenv
import pypdf, chromadb, anthropic

load_dotenv()
print("pypdf:", pypdf.__version__)
print("chromadb:", chromadb.__version__)
print("API key loaded:", bool(os.getenv("ANTHROPIC_API_KEY")))

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=20,
    messages=[{"role": "user", "content": "Say 'setup works'"}],
)
print(msg.content[0].text)