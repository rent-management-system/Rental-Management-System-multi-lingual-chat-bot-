

# API Documentation: Multilingual Chatbot

This document provides detailed information about the `/chat` endpoint for integration purposes.

---

## Chat Endpoint

### Method
`POST`

### Path
`/chat`

### Permissions
Public. No authentication is required to access this endpoint.

### User Types
This endpoint is available to all user types, including tenants, landlords, and the general public.

### Position in Code
- **Endpoint Definition**: `app/main.py` within the `chat_endpoint` function.
- **Core Logic**: The chatbot's reasoning and response generation is handled by a LangGraph graph defined in `app/chatbot_graph.py`.
- **Request Validation**: The request body is defined by the `ChatRequest` Pydantic model in `app/models.py`.

### Parameters

The endpoint expects a JSON body with the following fields:

| Parameter | Type   | Required | Description                                                                                                                                 |
|-----------|--------|----------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `query`   | string | Yes      | The question or message from the user. Must be at least 1 character long.                                                                   |
| `language`| string | No       | The language of the query. Supported values are `"english"`, `"amharic"`, and `"afaan_oromo"`. This field is **case-insensitive**. If omitted, the language is treated as English. |

#### Request Body Schema

```json
{
  "query": "string",
  "language": "string"
}
```

### Examples

Below are `curl` command examples demonstrating how to interact with the endpoint.

#### 1. English Query

This example asks a question in English.

```bash
curl -X 'POST' \
  'http://localhost:8012/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "How do I register as a new user?",
  "language": "english"
}'
```

#### 2. Amharic Query

This example asks a question in Amharic.

```bash
curl -X 'POST' \
  'http://localhost:8012/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "አዲስ ተጠቃሚ እንዴት መመዝገብ እችላለሁ?",
  "language": "amharic"
}'
```

#### 3. Afaan Oromo Query

This example asks a question in Afaan Oromo.

```bash
curl -X 'POST' \
  'http://localhost:8012/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "Akkaataa itti fayyadamaa haaraa ta'ee galmaa'uu danda'uu?",
  "language": "afaan_oromo"
}'
```

#### 4. Case-Insensitive Language Handling

This example shows that the `language` field is case-insensitive. The API will correctly interpret `"Amharic"` as `"amharic"`.

```bash
curl -X 'POST' \
  'http://localhost:8012/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "አዲስ ተጠቃሚ እንዴት መመዝገብ እችላለሁ?",
  "language": "Amharic"
}'
```

#### 5. Language Omitted (Defaults to English)

If the `language` field is omitted, the system defaults to English for processing the query and generating the response.

```bash
curl -X 'POST' \
  'http://localhost:8012/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What property types can I list?"
}'
```

