# README

## What happens when you run `python pipeline.py`?

**Short answer:** you pass a single `{"query": ...}` into the chain, and **LangChain’s `RetrievalQA`** automatically fills the two variables your prompt expects—`{context}` and `{question}`—behind the scenes.

---

## High-level flow

```
"query" (your input)
      │
      ▼
Retriever (vector store search)
      │
      ▼
Relevant Documents
      │
      ▼
Prompt Template expects:
  - {context}  ← concatenated docs ("stuffed" in)
  - {question} ← your original query
      │
      ▼
LLM call
      │
      ▼
Answer (+ optional source docs)
```

---

## Step-by-step execution

1. **Pipeline bootstraps (`pipeline.py`)**  
   - Loads/opens your vector store (persisted index).  
   - Creates a retriever.  
   - Instantiates your `AnimeRecommender` with the retriever and LLM config.

2. **Recommender builds a `RetrievalQA` chain (`recommender.py`)**  
   - Creates the LLM (e.g., `ChatGroq`).  
   - Loads your **custom prompt** which requires **two** variables: `{context}` and `{question}` (from `prompt_template.py`).  
   - Constructs:
     ```python
     RetrievalQA.from_chain_type(
         llm=llm,
         retriever=retriever,
         chain_type="stuff",
         chain_type_kwargs={"prompt": prompt},
         return_source_documents=True
     )
     ```
     - This sets up a **“stuff”** combine step that knows how to take documents from the retriever and **“stuff”** them into the prompt’s`{context}` variable.

3. **You call the chain with just `query`**  
   - `qa_chain.invoke({"query": "your search here"})`  
   - Internally, `RetrievalQA`:
     - uses the retriever to fetch relevant docs for the **query**,  
     - concatenates them → **`{context}`**,  
     - passes your original **`query`** through as **`{question}`** for the prompt,  
     - formats your prompt and calls the LLM,  
     - returns the final **answer**  **'result["result"]'** (and `source_documents` if requested).

So even though your PromptTemplate expects two inputs, you don’t manually supply them. RetrievalQA maps your single query to {question} and builds {context} from retrieved documents, then formats your prompt_template.py accordingly.
---

## Why the prompt takes `{context}` and `{question}` while you only pass `query`

- **You** supply **one input**: `query`.  
- **RetrievalQA**:
  - maps `query` → `{question}`,  
  - builds `{context}` from retrieved documents.  

That’s why your prompt template can require two variables even though your public chain interface takes one.

---

## Minimal usage example

```python
result = qa_chain.invoke({"query": "Recommend slice-of-life anime with strong character development"})
print(result["result"])
# Optional: inspect sources
for d in result.get("source_documents", []):
    print(d.metadata.get("source"), d.page_content[:200], "...")
```

Under the hood for that call:

```text
question = "Recommend slice-of-life anime with strong character development"
context  = "<concatenation of the top-N retrieved chunks>"
```

---

## Debugging tips

- **Turn on verbose tracing** when constructing the chain:
  ```python
  qa_chain = RetrievalQA.from_chain_type(
      llm=llm,
      retriever=retriever,
      chain_type="stuff",
      chain_type_kwargs={"prompt": prompt},
      return_source_documents=True,
      verbose=True,  # ← see internal steps & formatted prompts
  )
  ```
- **Print retrieved docs** right before the LLM call to see exactly what goes into `{context}`.
- **Sanity-check your prompt variables**: make sure only `{context}` and `{question}` appear in the template when using `RetrievalQA`.

---

## Common gotcha

- In `pipeline.py`, double-check the argument name for your vector store persistence directory. If you see something like `perist_dir=...` (missing the second “s”), fix it to `persist_dir=...` to match the class’ expected parameter.

---

## TL;DR

- You **invoke** with `{"query": ...}`.  
- `RetrievalQA` **retrieves docs** → builds `{context}` and uses your `query` as `{question}`.  
- Your prompt **requires two fields**, but you **only provide one**—the chain fills in the rest automatically.
