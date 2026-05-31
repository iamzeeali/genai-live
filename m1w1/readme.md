# OpenAI Tokenization, Embeddings, and Sampling Demo

This project demonstrates three fundamental concepts behind Large Language Models (LLMs):

1. **Tokenization** using `tiktoken`
2. **Embeddings** and vector arithmetic (`king - man + woman ≈ queen`)
3. **Text generation** using different temperature settings

---

## Prerequisites

* Python 3.9+
* OpenAI API key

---

## Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

Install dependencies:

```bash
pip install openai python-dotenv numpy tiktoken
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

# Part 1: Tokenization

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

text = "The capital of France is Paris."

tokens = enc.encode(text)

print(tokens)
print(enc.decode_tokens_bytes(tokens))
print(f"Token count: {len(tokens)}")
```

## What this demonstrates

LLMs do not read text as words.

They read text as **tokens**.

Example:

```text
"The capital of France is Paris."
```

may be split into chunks such as:

```text
"The"
" capital"
" of"
" France"
" is"
" Paris"
"."
```

The tokenizer converts text into token IDs that the model can process.

---

# Part 2: Embeddings

```python
response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
)
```

Embeddings convert text into high-dimensional vectors.

Example:

```python
king = embed("king")
man = embed("man")
woman = embed("woman")
queen = embed("queen")
```

---

## Vector Arithmetic

One famous property of embeddings is semantic arithmetic:

```python
result = king - man + woman
```

Conceptually:

```text
king
- man
+ woman
≈ queen
```

This works because embeddings capture relationships between concepts in vector space.

---

## Cosine Similarity

To compare vectors, we use cosine similarity:

```python
def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )
```

A similarity score:

* `1.0` → identical direction
* `0.0` → unrelated
* `-1.0` → opposite direction

Example:

```python
cosine_similarity(result, queen)
```

Expected outcome:

```text
king - man + woman
```

should be much closer to:

```text
queen
```

than to:

```text
Paris
```

---

# Part 3: Text Generation

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Complete: The capital of France is"
        }
    ],
    temperature=1.5
)

print(response.choices[0].message.content)
```

---

## Temperature

Temperature controls randomness during generation.

### Temperature = 0

The model behaves deterministically:

```text
Always choose the most likely next token.
```

Mental model:

```text
No dice roll.
```

---

### Temperature = 1

Normal randomness.

```text
Mostly likely answers,
with some variation.
```

---

### Temperature > 1

More creative and diverse outputs.

```text
More risk,
more variety,
more surprises.
```

---

# Key Concepts

## Token

A token is the basic unit processed by an LLM.

Mental model:

```text
Words are for humans.
Tokens are for models.
```

---

## BPE (Byte Pair Encoding)

BPE builds a vocabulary by repeatedly merging frequently occurring text fragments.

Mental model:

```text
BPE decides the ideal size of text chunks.
```

---

## Embedding

An embedding is a numerical representation of text.

Mental model:

```text
Text → Coordinates in semantic space
```

---

## Cosine Similarity

Measures how similar two vectors are.

Mental model:

```text
Same direction = similar meaning
```

---

## Temperature

Controls randomness during generation.

Mental model:

```text
How willing the model is
to choose less-likely tokens.
```

---

# Example Output

```text
Token count: 7

king-man+woman vs queen similarity:
0.84

king-man+woman vs paris similarity:
0.12

Paris.
```

Actual values will vary between runs and embedding models.

---

# Learning Goals

By completing this project, you will understand:

* How tokenization works
* What BPE is
* How embeddings represent meaning
* Why vector arithmetic works
* What cosine similarity measures
* How temperature affects generation
* The difference between deterministic and stochastic decoding

```
```
