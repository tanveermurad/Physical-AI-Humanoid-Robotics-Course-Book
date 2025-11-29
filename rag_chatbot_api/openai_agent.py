"""
OpenAI Agents SDK integration with Qdrant retrieval tool
for Physical AI & Humanoid Robotics chatbot
"""

from openai import AsyncOpenAI
from typing import List, Dict, Optional
import json
import os
import asyncio

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define Qdrant retrieval tool for function calling
QDRANT_TOOL = {
    "type": "function",
    "function": {
        "name": "search_course_content",
        "description": "Search the Physical AI & Humanoid Robotics course material for relevant information. Use this when you need specific information from the course to answer a question.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant course content. Should be specific and focused."
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return (default 5, max 10)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
}


async def search_qdrant_tool(query: str, num_results: int = 5):
    """
    Tool function to search Qdrant vector database

    Args:
        query: Search query string
        num_results: Number of results to return

    Returns:
        List of dicts with content and source
    """
    from qdrant_client_config import get_qdrant_client
    from langchain_qdrant import QdrantVectorStore
    from rag_core import get_embeddings

    try:
        qdrant_client = get_qdrant_client()
        embeddings = get_embeddings()

        vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name=os.getenv("QDRANT_COLLECTION_NAME", "book_content"),
            embedding=embeddings
        )

        # Perform similarity search
        docs = await vector_store.asimilarity_search(query, k=min(num_results, 10))

        # Format results
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown")
            })

        return results
    except Exception as e:
        print(f"Error searching Qdrant: {e}")
        return []


def build_system_prompt(user_profile: Optional[Dict] = None) -> str:
    """
    Build personalized system prompt based on user profile

    Args:
        user_profile: Dict with user background info (programmingExperience, rosExperience, etc.)

    Returns:
        Personalized system prompt string
    """
    base_prompt = """You are an expert tutor for Physical AI and Humanoid Robotics.
Your goal is to educate students about robotics, ROS 2, computer vision, humanoid systems, and physical AI.

Guidelines:
- Be clear, educational, and encouraging
- Provide code examples when relevant (Python, C++, ROS 2)
- Reference specific chapters or concepts from the course material
- Admit when you don't know something rather than making up information
- When appropriate, use the search_course_content tool to find relevant information from the course
- Break down complex topics into understandable parts"""

    if not user_profile:
        return base_prompt

    # Extract user experience levels
    prog_exp = user_profile.get('programmingExperience', 'intermediate')
    ros_exp = user_profile.get('rosExperience', 'none')
    ai_ml_exp = user_profile.get('aiMlExperience', 'none')

    personalization = f"""

USER CONTEXT:
- Programming experience: {prog_exp}
- ROS experience: {ros_exp}
- AI/ML experience: {ai_ml_exp}

ADAPTATION INSTRUCTIONS:"""

    # Adjust based on programming experience
    if prog_exp == 'beginner':
        personalization += """
- Explain concepts step-by-step with basic terminology
- Provide simple code examples with detailed comments
- Define technical terms when first introducing them
- Use analogies to explain abstract concepts"""
    elif prog_exp in ['advanced', 'expert']:
        personalization += """
- Use advanced terminology and assume strong programming knowledge
- Focus on best practices, optimizations, and design patterns
- Provide concise explanations without over-simplifying
- Discuss trade-offs and alternative approaches"""

    # Adjust based on ROS experience
    if ros_exp == 'none':
        personalization += """
- Explain ROS concepts from the ground up
- Link to ROS tutorials when relevant (http://wiki.ros.org/ROS/Tutorials)
- Define ROS-specific terms (nodes, topics, services, actions)
- Provide context for why ROS is used in robotics"""
    elif ros_exp == 'advanced':
        personalization += """
- Assume solid ROS knowledge, skip basic explanations
- Focus on advanced ROS 2 patterns and architectural decisions
- Discuss DDS, Quality of Service, and performance considerations
- Reference ROS 2 best practices"""

    # Adjust based on AI/ML experience
    if ai_ml_exp == 'none':
        personalization += """
- Explain AI/ML concepts accessibly
- Provide intuitive explanations of algorithms
- Suggest beginner-friendly resources for machine learning"""
    elif ai_ml_exp in ['intermediate', 'advanced']:
        personalization += """
- Use ML terminology naturally
- Discuss model architectures, training strategies, and evaluation metrics
- Reference recent research when relevant"""

    return base_prompt + personalization


async def chat_with_agent(
    message: str,
    selected_text: Optional[str] = None,
    user_profile: Optional[Dict] = None,
    chat_history: Optional[List[Dict]] = None
) -> Dict:
    """
    Chat with OpenAI Agent using tools and personalization

    Args:
        message: User's question/message
        selected_text: Text selected by user from the course (if any)
        user_profile: User's background information for personalization
        chat_history: Previous conversation messages

    Returns:
        Dict with:
            - response: str (agent's answer)
            - sources: List[str] (unique sources used)
            - tool_calls: List[str] (for debugging, shows what tools were called)
    """

    # Build messages array
    messages = [
        {"role": "system", "content": build_system_prompt(user_profile)}
    ]

    # Add chat history if provided
    if chat_history:
        messages.extend(chat_history)

    # Build user message, incorporating selected text if provided
    user_message = message
    if selected_text:
        user_message = f"""The user has selected this text from the course:

\"\"\"{selected_text}\"\"\"

Question about the selected text: {message}

Please answer their question with specific reference to this selected content. If you need additional context, use the search_course_content tool."""

    messages.append({"role": "user", "content": user_message})

    # Initial API call with tools
    response = await client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        tools=[QDRANT_TOOL],
        tool_choice="auto",  # Let the agent decide when to use tools
        temperature=0.3  # Lower temperature for more focused, educational responses
    )

    assistant_message = response.choices[0].message
    tool_calls_made = []
    sources = []

    # Handle tool calls (agentic loop)
    # The agent can call tools multiple times if needed
    while assistant_message.tool_calls:
        # Append assistant's message with tool calls
        messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in assistant_message.tool_calls
            ]
        })

        # Execute each tool call
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name == "search_course_content":
                # Execute Qdrant search
                results = await search_qdrant_tool(
                    query=function_args.get("query"),
                    num_results=function_args.get("num_results", 5)
                )

                # Track sources
                sources.extend([r["source"] for r in results])

                # Format tool response
                tool_response = {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(results, indent=2)
                }

                messages.append(tool_response)
                tool_calls_made.append(f"Searched: {function_args.get('query')}")

        # Get next response after tool execution
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            tools=[QDRANT_TOOL],
            tool_choice="auto",
            temperature=0.3
        )

        assistant_message = response.choices[0].message

    # Return final response
    return {
        "response": assistant_message.content or "",
        "sources": list(set(sources)),  # Unique sources
        "tool_calls": tool_calls_made  # For debugging/logging
    }


# Helper function for formatting chat history from frontend
def format_chat_history_for_agent(chat_history: List[Dict]) -> List[Dict]:
    """
    Format chat history from frontend format to OpenAI API format

    Args:
        chat_history: List of ChatMessage dicts from frontend

    Returns:
        List of message dicts in OpenAI format
    """
    formatted = []
    for msg in chat_history:
        formatted.append({
            "role": msg.get("role"),
            "content": msg.get("content")
        })
    return formatted
