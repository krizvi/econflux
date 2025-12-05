## RAG Context Example

In Retrieval-Augmented Generation (RAG) systems, it's standard practice to combine retrieved chunks (relevant text snippets or documents from a knowledge base) with the user's query or prompt into a single prompt sent to the LLM for generation. However, there's no universally standardized "industry or technical format" for how this is done—implementations vary based on the framework, API, or custom system.

### Common Approaches:
- **Embedded Context**: Retrieved chunks are concatenated or inserted into a prompt template. For example:
  ```
  Context: [Chunk 1 text][Chunk 2 text]...
  Question: [User query]
  Answer:
  ```
  This combined string is sent to the LLM via its API (e.g., OpenAI, Anthropic, or local models).

- **Structured Formats**: Some systems use JSON-like structures if the LLM supports tool calling or structured inputs, but this isn't specific to RAG—it's more about how data is passed in general. For instance, with OpenAI's API, you might include context in the `messages` array as system or user prompts.

- **No Formal Protocol**: Unlike something like HTTP headers or database schemas, there's no official protocol or schema for RAG prompts. Popular libraries like LangChain, LlamaIndex, or Haystack provide patterns, but they're configurable. For example:
  - LangChain uses prompt templates that can interpolate retrieved documents.
  - Vector databases (e.g., Pinecone, Weaviate) often have query methods that return chunks which you then format into prompts.

If you're implementing RAG and need help with a specific format or integrating it into your code (e.g., in the `aws-agentcore-gateway` project I'm seeing), provide more details about your setup, and I can assist with the implementation.

---

Here's a realistic example of a typical context/prompt sent to an LLM in a RAG system. This assumes a conversational setup where retrieved chunks (e.g., from a knowledge base about AWS services) are embedded into the prompt. The format can vary, but this is a common pattern used in frameworks like LangChain or custom implementations:

---

**System Prompt:**

```
You are a helpful AI assistant specializing in AWS services. Use the provided context to answer questions accurately. If the context doesn't contain sufficient information, say so.
```

**Context (Retrieved Chunks):**

```
Chunk 1: AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. It supports multiple languages like Python, Node.js, and Java.

Chunk 2: Lambda functions can be triggered by events from AWS services such as S3, DynamoDB, or API Gateway. You can set up HTTP endpoints using API Gateway to invoke Lambda functions via REST or WebSocket APIs.

Chunk 3: Pricing for Lambda is based on the number of requests and compute time (in GB-seconds). The first 1 million requests per month are free, after which it's $0.20 per 1 million requests. Compute time costs $0.00001667 per GB-second.
```

**User Query:**

```
How does AWS Lambda pricing work, and can it be integrated with API Gateway?
```

**Full Prompt Sent to LLM:**

```
You are a helpful AI assistant specializing in AWS services. Use the provided context to answer questions accurately. If the context doesn't contain sufficient information, say so.

Context:
Chunk 1: AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. It supports multiple languages like Python, Node.js, and Java.

Chunk 2: Lambda functions can be triggered by events from AWS services such as S3, DynamoDB, or API Gateway. You can set up HTTP endpoints using API Gateway to invoke Lambda functions via REST or WebSocket APIs.

Chunk 3: Pricing for Lambda is based on the number of requests and compute time (in GB-seconds). The first 1 million requests per month are free, after which it's $0.20 per 1 million requests. Compute time costs $0.00001667 per GB-second.

Question: How does AWS Lambda pricing work, and can it be integrated with API Gateway?
```

**Expected LLM Response:**

```
Based on the provided context, AWS Lambda pricing is based on the number of requests and compute time (measured in GB-seconds). The first 1 million requests per month are free, followed by $0.20 per additional 1 million requests. Compute time costs $0.00001667 per GB-second. 

Yes, Lambda can be integrated with API Gateway, where Lambda functions can be triggered by API Gateway events, allowing you to set up HTTP endpoints.
```

---

In practice, the chunks might be ranked by relevance, truncated to fit token limits, or filtered to the most relevant ones. This approach reduces hallucinations by grounding the response in retrieved data while keeping the process efficient.