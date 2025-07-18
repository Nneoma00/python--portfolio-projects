#write a haiku

from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

#print(completion.choices[0].message);
print(completion.choices[0].message.content)