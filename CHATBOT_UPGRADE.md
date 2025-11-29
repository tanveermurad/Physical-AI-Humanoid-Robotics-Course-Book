# Chatbot Upgrade Guide

Complete guide for the upgraded RAG chatbot with OpenAI Agents SDK, Neon Serverless Postgres, text selection, and personalized responses.

## 🎯 Overview

The upgraded chatbot includes:
- ✅ **OpenAI Agents SDK** with custom Qdrant retrieval tool
- ✅ **Neon Serverless Postgres** for chat history storage
- ✅ **Text Selection** - Answer questions about user-selected text
- ✅ **Personalization** - Responses adapt to user's programming/ROS experience
- ✅ **Qdrant Cloud** - Vector search for course content (already configured!)

## 📋 Prerequisites

### Required Accounts
1. **OpenAI Account** - For GPT-4 API access
2. **Neon Account** - For serverless Postgres database
3. **Qdrant Cloud** - Already set up! ✅

### Required Software
- Python 3.9+
- Node.js 20+
- npm or yarn

## 🚀 Setup Instructions

### Step 1: Set Up Neon Database

#### 1.1 Create Neon Account
1. Go to [https://neon.tech](https://neon.tech)
2. Sign up with GitHub or email
3. Verify your email

#### 1.2 Create Project
1. Click **"Create Project"**
2. **Project Name**: `physical-ai-chatbot`
3. **Region**: Choose closest to your users (e.g., `us-east-1`)
4. **Postgres Version**: 15 (default)
5. Click **"Create Project"**

#### 1.3 Get Connection String
1. In the project dashboard, click **"Connection Details"**
2. Copy the connection string (it looks like):
   ```
   postgresql://username:password@ep-xxx-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```
3. **IMPORTANT**: Save the password! It won't be shown again.

#### 1.4 Convert for SQLAlchemy
Change the connection string to use `asyncpg` driver:
```
postgresql+asyncpg://username:password@ep-xxx-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Step 2: Get OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click **"Create new secret key"**
3. Name it: `physical-ai-chatbot`
4. Copy the API key (starts with `sk-...`)
5. **IMPORTANT**: Save it somewhere safe!

### Step 3: Update Backend Environment

Edit `rag_chatbot_api/.env`:

```env
# OpenAI API Key
OPENAI_API_KEY=sk-proj-...your-key-here...

# Neon Postgres Connection String
DATABASE_URL=postgresql+asyncpg://username:password@host.neon.tech/neondb?sslmode=require

# Qdrant Cloud (already configured)
QDRANT_API_KEY=your-existing-key
QDRANT_HOST=https://your-cluster.aws.cloud.qdrant.io:6333
QDRANT_COLLECTION_NAME=book_content

# Model Configuration
EMBEDDING_MODEL_NAME=gemini
LLM_MODEL_NAME=gemini
```

### Step 4: Install Backend Dependencies

```bash
cd rag_chatbot_api
pip install -r requirements.txt
```

This will install:
- `openai>=1.0.0` - OpenAI Agents SDK
- `asyncpg` - PostgreSQL async driver
- All existing dependencies

### Step 5: Initialize Database

The database schema will be created automatically on first startup:

```bash
cd rag_chatbot_api
python main.py
```

You should see:
```
Initializing database...
Database initialized.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Test Backend

In another terminal:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is ROS 2?",
    "user_profile": {
      "programmingExperience": "beginner",
      "rosExperience": "none"
    }
  }'
```

You should get a personalized response!

### Step 7: Start Frontend

```bash
cd my-book
npm start
```

The site opens at `http://localhost:3000`.

## 🧪 Testing the Features

### Test 1: Basic Chat
1. Open chatbot (bottom-right button)
2. Ask: "What is ROS 2?"
3. ✅ Verify you get a response with sources

### Test 2: Text Selection
1. Navigate to any course chapter
2. **Select some text** by highlighting it
3. Click the chatbot button
4. ✅ Verify selected text appears in blue banner
5. Ask a question about the selected text
6. ✅ Verify response references your selection

### Test 3: Personalization (Signed In)
1. **Sign in** to your account
2. Go to **Profile** and set:
   - Programming experience: **Beginner**
   - ROS experience: **None**
3. Open chatbot
4. Ask: "How do I create a ROS node?"
5. ✅ Verify response is beginner-friendly with step-by-step explanation

### Test 4: Personalization (Advanced User)
1. Update profile:
   - Programming experience: **Advanced**
   - ROS experience: **Advanced**
2. Ask same question: "How do I create a ROS node?"
3. ✅ Verify response assumes knowledge, focuses on advanced patterns

### Test 5: Tool Calling
1. Ask: "Tell me about Isaac Sim"
2. ✅ In terminal, you should see the agent call `search_course_content` tool
3. ✅ Response should include specific information from the course

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User (Signed In)                          │
│  • Has profile (programming/ROS experience)                  │
│  • Selects text from chapter                                 │
└────────────────────┬────────────────────────────────────────┘
                     │ Opens chatbot
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              Frontend Chatbot Component                      │
│  • Captures selected text                                    │
│  • Shows selected text banner                                │
│  • Builds user profile from auth context                     │
│  • Sends to /chat endpoint                                   │
└────────────────────┬────────────────────────────────────────┘
                     │ POST /chat
                     │ {
                     │   message,
                     │   selected_text,
                     │   user_profile,
                     │   user_id
                     │ }
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              Backend (FastAPI main.py)                       │
│  • Receives request                                          │
│  • Calls openai_agent.chat_with_agent()                     │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│           OpenAI Agent (openai_agent.py)                     │
│                                                              │
│  1. Build personalized system prompt                         │
│     ├─ Adapt to programming experience                      │
│     ├─ Adapt to ROS experience                              │
│     └─ Adapt to AI/ML experience                            │
│                                                              │
│  2. Prepare user message                                     │
│     └─ If selected_text: wrap question with context         │
│                                                              │
│  3. Call OpenAI with tools=[QDRANT_TOOL]                    │
│     Agent decides: Need more context?                        │
│         ↙                          ↘                         │
│       Yes                          No                        │
│        ↓                            ↓                        │
│  Call search_course_content    Use existing context         │
│        ↓                            ↓                        │
│  Execute Qdrant search          Generate response           │
│        ↓                            ↓                        │
│  Return results to agent       ────┘                        │
│        ↓                                                     │
│  Agent generates final response                              │
│                                                              │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│               Neon Postgres Database                         │
│  • Stores chat history                                       │
│  • Links to user_id                                          │
│  • Saves selected_text                                       │
│  • Metadata: sources, tool_calls, user_profile              │
└─────────────────────────────────────────────────────────────┘
                     ↓
                Returns to frontend
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              Display Response                                │
│  • Shows AI answer                                           │
│  • Lists sources used                                        │
│  • Clears selected text banner                              │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Database Schema

### ChatHistory Table

| Column             | Type     | Description                                |
|--------------------|----------|--------------------------------------------|
| `id`               | Integer  | Primary key                                |
| `session_id`       | String   | Session identifier                         |
| `user_id`          | String   | User ID from Better Auth (nullable)        |
| `user_message`     | Text     | User's question                            |
| `assistant_message`| Text     | AI's response                              |
| `selected_text`    | Text     | Text selected by user (nullable)           |
| `metadata`         | JSON     | Sources, tool calls, user profile          |
| `timestamp`        | DateTime | Auto-generated timestamp                   |

## 🎨 Personalization Examples

### Example 1: Beginner + No ROS

**User Profile:**
- Programming Experience: Beginner
- ROS Experience: None

**Question:** "How do I create a ROS node?"

**Agent's System Prompt Includes:**
- Explain concepts step-by-step with basic terminology
- Provide simple code examples with detailed comments
- Explain ROS concepts from the ground up
- Link to ROS tutorials when relevant

**Response Style:**
```
A ROS node is a process that performs computation in your robot system.
Think of it as a program that communicates with other programs.

Here's a simple example:

```python
import rclpy  # Import ROS 2 Python library
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')  # Give your node a name
        self.get_logger().info('Node started!')  # Print a message

def main():
    rclpy.init()  # Initialize ROS 2
    node = MyNode()  # Create your node
    rclpy.spin(node)  # Keep it running
```

Let me explain each part...
```

### Example 2: Advanced + Expert ROS

**User Profile:**
- Programming Experience: Advanced
- ROS Experience: Advanced

**Same Question:** "How do I create a ROS node?"

**Agent's System Prompt Includes:**
- Use advanced terminology
- Assume solid ROS knowledge, skip basic explanations
- Focus on advanced ROS 2 patterns
- Discuss DDS, Quality of Service

**Response Style:**
```
For ROS 2 node creation, you'll use rclcpp or rclpy with the Node class.
Key architectural considerations:

- QoS policies for reliable vs. best-effort communication
- Executor patterns (single-threaded, multi-threaded, or callback groups)
- Component-based architecture for better composability

Example with QoS configuration:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy

qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
self.publisher = self.create_publisher(MyMsg, 'topic', qos)
```

Consider lifecycle nodes if you need managed state transitions...
```

## 🔧 Advanced Configuration

### Adjust Model Selection

In `openai_agent.py`, line 254:
```python
response = await client.chat.completions.create(
    model="gpt-4-turbo-preview",  # Change model here
    messages=messages,
    tools=[QDRANT_TOOL],
    tool_choice="auto",
    temperature=0.3  # Adjust temperature (0.0-1.0)
)
```

**Model Options:**
- `gpt-4-turbo-preview` - Best quality (current default)
- `gpt-4` - Stable version
- `gpt-3.5-turbo` - Faster, cheaper (for simple queries)

### Customize Tool Behavior

In `openai_agent.py`, modify `QDRANT_TOOL` definition:
```python
QDRANT_TOOL = {
    "type": "function",
    "function": {
        "name": "search_course_content",
        "description": "Your custom description here",  # Edit this
        "parameters": {
            # Adjust parameters
        }
    }
}
```

### Add More Personalization Fields

In `openai_agent.py`, `build_system_prompt()` function:
```python
# Extract more user fields
hardware_exp = user_profile.get('roboticsExperience', 'none')

# Add custom adaptations
if hardware_exp == 'professional':
    personalization += """
- Reference industry standards and production considerations
- Discuss safety, reliability, and testing strategies"""
```

## 💰 Cost Estimates

### OpenAI API Costs

**GPT-4 Turbo Preview:**
- Input: $0.01 per 1K tokens
- Output: $0.03 per 1K tokens

**Typical Query:**
- User question: ~50 tokens
- System prompt: ~200 tokens
- Retrieved context: ~1000 tokens
- Response: ~300 tokens
- **Total cost per query**: ~$0.02

**Monthly estimates:**
- 100 queries/day = $60/month
- 500 queries/day = $300/month
- 1000 queries/day = $600/month

### Neon Postgres Costs

**Free Tier:**
- 0.5 GB storage
- 100 compute hours/month
- ~500K chat messages

**Paid (if exceeded):**
- $0.16/GB storage per month
- $0.16/compute hour

**Typical usage**: Free tier sufficient for most use cases!

### Qdrant Cloud

**Already using free tier!** ✅
- 1 GB storage
- 1M vectors
- No additional cost

## 🐛 Troubleshooting

### Issue: "OpenAI API key not found"

**Solution:**
```bash
cd rag_chatbot_api
echo "OPENAI_API_KEY=sk-..." >> .env
```

### Issue: "Database connection error"

**Symptoms:** `AsyncioError: Unable to connect to database`

**Solution:**
1. Verify Neon connection string in `.env`
2. Check it includes `asyncpg` driver:
   ```
   postgresql+asyncpg://...
   ```
3. Ensure Neon project is not paused (free tier auto-pauses after inactivity)

### Issue: "Selected text not captured"

**Solution:**
1. Ensure you're highlighting text **before** opening chatbot
2. Selected text must be >10 characters
3. Check browser console for JavaScript errors

### Issue: "Responses not personalized"

**Solution:**
1. Ensure you're **signed in**
2. Check profile has background filled in
3. Verify user profile is passed in network request (check browser dev tools)

### Issue: "Agent not calling Qdrant tool"

**Symptoms:** Agent responds without searching course content

**This is normal!** The agent decides when to call tools. It may:
- Use selected text directly (no search needed)
- Answer from general knowledge
- Call tool for specific course questions

To force tool usage, ask: "What does the course say about X?"

### Issue: "Chat history not saving"

**Solution:**
1. Check Neon connection in terminal logs
2. Verify `DATABASE_URL` in `.env`
3. Check Neon project is active (not paused)

## 📚 API Reference

### POST /chat

**Request:**
```json
{
  "message": "What is ROS 2?",
  "chat_history": [
    {"role": "user", "content": "Previous question"},
    {"role": "assistant", "content": "Previous answer"}
  ],
  "selected_text": "ROS 2 is a flexible framework...",
  "user_profile": {
    "programmingExperience": "beginner",
    "rosExperience": "none",
    "aiMlExperience": "basic"
  },
  "user_id": "user123"
}
```

**Response:**
```json
{
  "response": "ROS 2 (Robot Operating System 2) is...",
  "source_documents": [
    "docs/ros2-intro.md",
    "docs/ros2-architecture.md"
  ],
  "chat_history": [
    {"role": "user", "content": "What is ROS 2?"},
    {"role": "assistant", "content": "ROS 2 is..."}
  ]
}
```

## 🎓 Usage Tips

### For Students

1. **Sign up and fill out your profile** - Get better personalized responses!
2. **Select text before asking** - Get answers specific to that content
3. **Build on conversation** - The chatbot remembers your chat history
4. **Check sources** - Click "Source Documents" to see where answers come from

### For Instructors

1. **Monitor chat history** in Neon dashboard
2. **Adjust system prompts** in `openai_agent.py` for your teaching style
3. **Add more personalization** based on student backgrounds
4. **Track common questions** to improve course content

## 🚀 Next Steps

### Enhancements to Consider

1. **Voice Input** - Add Whisper API for voice questions
2. **Multi-language** - Translate responses to student's language
3. **Image Support** - Let users ask about diagrams/code screenshots
4. **Code Execution** - Run and test code snippets in chat
5. **Progress Tracking** - Track which topics students ask about most

### Production Deployment

See main `README.md` for deployment instructions to:
- Vercel/Netlify (frontend)
- Railway/Render (backend)
- Keep Neon Postgres (already cloud-ready!)

## 📝 Related Documentation

- [IMPLEMENTATION_PROGRESS.md](IMPLEMENTATION_PROGRESS.md) - Current status
- [AUTHENTICATION_SETUP.md](AUTHENTICATION_SETUP.md) - Auth setup
- [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) - Urdu translation
- [PERSONALIZATION_EXAMPLE.md](PERSONALIZATION_EXAMPLE.md) - Chapter personalization
- [README.md](README.md) - Main project documentation

---

**Questions?** Open an issue on GitHub or check the plan file at `.claude/plans/keen-percolating-deer.md`
