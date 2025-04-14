#OpenAI LLM Agent Chatbot

This is an OpenAI API-based chatbot application that allows users to interact with multiple domain-specific agents. Each agent specializes in a different area, providing intelligent and human-like responses. The chatbot runs from the Chatbot.py file, where users can choose the type of agent they'd like to interact with.
Features

- Switch between multiple intelligent agents
- Leverages OpenAI's powerful GPT-4 model
- Gmail integration via OAuth
- Real-time weather Q&A
- Upload and query PDF documents
- Natural, conversational responses

  #Email Agent
  
- Integrates with **Gmail** using **OAuth 2.0**.
- Supports:
  - Sending emails
  - Reading unread messages
- Streaming enabled for real-time feedback.
- Note: May have minor glitches during use of stream.

Weather Agent
- Uses OpenAI to extract the **location** from the user’s query.
- Retrieves current weather details.
- Provides human-like descriptions of weather conditions.

Simple Agent
- General-purpose agent.
- Responds to common questions in a conversational style.
- Does not rely on external data sources.

Knowledge Base Agent
- Right now works with one of the uploaded fine :  A survey on deep learning-based algorithms for the traveling
 salesman problem
- Utilizes OpenAI's `file_id` and `response` apis for Q&A over the uploaded content.
- Best suited for academic papers, research summaries, or structured PDF content.

