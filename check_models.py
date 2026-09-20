from groq import Groq
from app.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


models = client.models.list()


print("\nAVAILABLE GROQ MODELS:\n")

for model in models.data:
    print(model.id)