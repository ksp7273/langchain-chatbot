# Chatbot Development Guide: Mistral-7B-Instruct-v0.3 with Hugging Face API

## Key Considerations for Choosing a Model

When selecting a model for a text generation chatbot using the Hugging Face API, consider the following:

1. **Performance and Coherence**: The model should generate contextually relevant, coherent, and engaging responses.
2. **Model Size and Resource Requirements**: Larger models perform better but require more computational resources, impacting API deployment.
3. **License and Commercial Use**: Ensure the model’s license aligns with your use case (commercial or non-commercial).
4. **Community Support and Fine-Tuning**: Models with active community support and fine-tuned versions for conversational tasks are preferable.
5. **Inference Support**: The model should be supported by Hugging Face’s Inference API or HuggingChat for seamless integration.

## Top Hugging Face Models for Chatbot Text Generation

Here are prominent models suitable for chatbot development on Hugging Face:

1. **Mistral-7B-Instruct-v0.3 (mistralai/Mistral-7B-Instruct-v0.3)**

   - **Description**: A 7-billion-parameter model fine-tuned for instruction-following, ideal for conversational tasks with coherent responses.
   - **Strengths**: Strong performance, lightweight (relative to larger models), Apache 2.0 license (commercial use allowed), supported by Hugging Face’s Inference Client.
   - **Use Case**: Ideal for chatbots needing concise, accurate responses.
   - **Challenges**: May require fine-tuning for domain-specific tasks.

2. **Meta Llama 3 70B (meta-llama/Llama-3-70b)**

   - **Description**: A 70-billion-parameter model with excellent reasoning and conversational abilities, available via HuggingChat.
   - **Strengths**: High-quality, human-like responses, strong LLM Leaderboard performance, supported by Text Generation Inference (TGI).
   - **Use Case**: Best for advanced chatbots (e.g., customer service).
   - **Challenges**: Resource-intensive, restrictive license (non-commercial).

3. **Mixtral 8x7B (mistralai/Mixtral-8x7B-Instruct-v0.1)**

   - **Description**: A mixture-of-experts model with 8x7 billion parameters, fine-tuned for instruction-following.
   - **Strengths**: Efficient MoE architecture, high-quality responses, Apache 2.0 license.
   - **Use Case**: Suitable for complex chatbot interactions with reasoning.
   - **Challenges**: Complex deployment due to architecture.

4. **BLOOM (bigscience/bloom)**

   - **Description**: A multilingual 176-billion-parameter model trained on 46 languages.
   - **Strengths**: Excellent for multilingual chatbots, open-source, permissive license.
   - **Use Case**: Ideal for chatbots targeting diverse linguistic audiences.
   - **Challenges**: Resource-intensive, challenging for API deployment.

5. **GPT-2 (openai-community/gpt2)**

   - **Description**: A smaller model (124M–1.5B parameters) for text generation, adaptable for chatbots.
   - **Strengths**: Lightweight, MIT license, easy to deploy.
   - **Use Case**: Good for prototyping or low-resource environments.
   - **Challenges**: Less coherent, requires fine-tuning.

## Recommended Model: Mistral-7B-Instruct-v0.3

**Why Mistral-7B-Instruct-v0.3?**

- **Performance**: Offers a strong balance of coherence and efficiency for conversational tasks.
- **Resource Efficiency**: 7 billion parameters require \~14GB GPU memory, practical for API deployment.
- **License**: Apache 2.0 allows commercial use.
- **Ease of Use**: Well-supported by Hugging Face’s Inference Client and Transformers library.
- **Community and Documentation**: Active support and detailed documentation for customization.

## Prerequisites for Both Environments

- **Hugging Face Account and API Token**: Obtain at https://huggingface.co/settings/tokens.
- **.env File**: Create with `HF_TOKEN=your_huggingface_api_token_here`.
- **Basic Familiarity**: Knowledge of Python and command-line operations.

## Step-by-Step Process: GitHub Codespaces

### Step 1: Set Up a GitHub Codespace

1. Create a repository on GitHub (e.g., `mistral-chatbot`).
2. Navigate to the repository, click **Code** &gt; **Codespaces** &gt; **Create codespace on main**.
3. A cloud-based VS Code environment with Python will launch.

### Step 2: Install Dependencies

1. Open the terminal (`Ctrl + ~`).
2. Install required libraries:

   ```bash
   pip install panel huggingface_hub python-dotenv aiohttp
   ```
3. Verify installation:

   ```bash
   pip list
   ```

   Ensure `panel`, `huggingface_hub`, `python-dotenv`, and `aiohttp` are listed.

### Step 3: Add the Chatbot Code

1. Create `chatbot.py`:

   ```bash
   touch chatbot.py
   ```
2. Write the chatbot code:

   ```bash
   cat << 'EOF' > chatbot.py
   import os
   import panel as pn
   from huggingface_hub import AsyncInferenceClient
   from dotenv import load_dotenv
   
   # Load environment variables from .env file
   load_dotenv()
   
   # Initialize the Hugging Face Inference Client
   client = AsyncInferenceClient(
       model="mistralai/Mistral-7B-Instruct-v0.3",
       token=os.environ.get("HF_TOKEN")
   )
   
   # System prompt to customize chatbot behavior
   SYSTEM_PROMPT = "You are a friendly and helpful assistant. Provide concise, accurate, and engaging responses."
   
   # Asynchronous callback function to handle chat interactions
   async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
       # Initialize conversation history
       messages = [{"role": "system", "content": SYSTEM_PROMPT}]
       
       # Add conversation history from Panel ChatInterface
       messages.extend([{"role": msg["role"], "content": msg["content"]} for msg in instance.serialize()[1:-1]])
       
       # Add the new user message
       messages.append({"role": "user", "content": contents})
       
       # Get response from Mistral-7B-Instruct-v0.3 (non-streaming)
       response = await client.chat_completion(messages=messages, max_tokens=500)
       message = response.choices[0].message.content
       yield message
   
   # Initialize Panel extension for web-based UI
   pn.extension()
   
   # Create the ChatInterface widget with verbose error handling
   chat_interface = pn.chat.ChatInterface(
       callback=callback,
       callback_user="Mistral",
       user="You",
       show_clear=False,
       show_undo=False,
       width=800,
       height=500,
       css_classes=["chat-interface"],
       callback_exception="verbose"
   )
   
   # Custom CSS for a polished UI
   pn.config.raw_css.append("""
   .chat-interface {
       background-color: #f5f5f5;
       border-radius: 10px;
       padding: 15px;
       font-family: Arial, sans-serif;
   }
   .chat-interface .pn-chat-message {
       border-radius: 8px;
       margin: 5px;
   }
   .chat-interface .pn-chat-message.user {
       background-color: #007bff;
       color: white;
   }
   .chat-interface .pn-chat-message.assistant {
       background-color: #e9ecef;
       color: black;
   }
   """)
   
   # Serve the chat interface
   chat_interface.servable()
   EOF
   ```
3. Create `.env` with your API token:

   ```bash
   echo "HF_TOKEN=your_huggingface_api_token_here" > .env
   ```
4. Verify files:

   ```bash
   ls -a
   ```

### Step 4: Run the Chatbot

1. Serve the application:

   ```bash
   panel serve chatbot.py --show
   ```
2. Interact with the chatbot in the browser UI.
3. Stop the server with `Ctrl + C`.

### Step 5: Test the Chatbot

1. Run:

   ```bash
   panel serve chatbot.py --show
   ```
2. Test prompts (e.g., “Tell me about Python”) and verify responses.

## Step-by-Step Fix in GitHub Codespaces

### Step 1: Install `aiohttp`

1. Open the terminal (`Ctrl + ~`).
2. Install `aiohttp`:

   ```bash
   pip install aiohttp
   ```
3. Verify:

   ```bash
   pip show aiohttp
   ```

### Step 2: Verify Existing Dependencies

1. Update dependencies:

   ```bash
   pip install --upgrade pip
   pip install --upgrade panel huggingface_hub python-dotenv aiohttp
   ```
2. Check versions:

   ```bash
   pip list | grep -E 'panel|huggingface_hub|python-dotenv|aiohttp'
   ```

### Step 3: Verify `.env` File

1. Check existence:

   ```bash
   ls -a
   ```
2. Verify contents:

   ```bash
   cat .env
   ```
3. Recreate if needed:

   ```bash
   echo "HF_TOKEN=your_huggingface_api_token_here" > .env
   ```

### Step 4: Verify `chatbot.py`

1. Check contents:

   ```bash
   cat chatbot.py
   ```
2. Ensure it matches the provided code.

### Step 5: Run the Chatbot

1. Run:

   ```bash
   panel serve chatbot.py --show
   ```
2. Test prompts and verify functionality.

## Step-by-Step Process to Save Code to a GitHub Repository

### Step 1: Verify Repository Setup

1. Check directory:

   ```bash
   pwd
   ```
2. Check Git status:

   ```bash
   git status
   ```

### Step 2: Initialize Git Repository (If Needed)

1. Initialize:

   ```bash
   git init
   ```
2. Verify:

   ```bash
   git status
   ```

### Step 3: Create or Update `.gitignore`

1. Create:

   ```bash
   touch .gitignore
   ```
2. Add exclusions:

   ```bash
   echo -e ".env\n__pycache__/\n*.pyc\n.python-version\nvenv/\n*.egg-info/\n.vscode/" > .gitignore
   ```

### Step 4: Create `requirements.txt`

1. Generate:

   ```bash
   echo -e "panel\nhuggingface_hub\npython-dotenv\naiohttp" > requirements.txt
   ```

### Step 5: Stage and Commit Files

1. Stage:

   ```bash
   git add chatbot.py .gitignore requirements.txt
   ```
2. Commit:

   ```bash
   git commit -m "Add chatbot code, gitignore, and requirements"
   ```

### Step 6: Link to Remote GitHub Repository

1. Check existing remote:

   ```bash
   git remote -v
   ```
2. If `origin` exists, update if needed:

   ```bash
   git remote set-url origin https://github.com/your-username/mistral-chatbot.git
   ```

### Step 7: Push to GitHub

1. Push:

   ```bash
   git push -u origin main
   ```
2. Verify on GitHub in your repository.