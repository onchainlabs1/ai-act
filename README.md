# AI Act Tutor - Developer Guide

An interactive Streamlit-based educational tool for studying and exploring the European Union AI Act (Regulation 2024/1689) through Retrieval-Augmented Generation (RAG), interactive quizzes, and guided study modules.

## 🎯 Project Overview

AI Act Tutor is designed to help AI practitioners, lawyers, policy students, and anyone interested in understanding the EU AI Act through an intuitive, AI-powered interface. The application leverages state-of-the-art RAG technology to provide accurate, citation-backed responses about the regulation.

## 🏗️ Project Structure

```
ai-act-tutor/
├── app/                    # Streamlit application modules
│   ├── main.py            # Entry point with multipage navigation
│   ├── chat.py            # RAG-powered chat interface
│   ├── study.py           # Guided study modules
│   └── quiz.py            # Interactive quiz system
├── core/                   # Core business logic
│   ├── loader.py          # Document loading and chunking
│   ├── rag_chain.py       # RAG chain construction
│   └── quiz_generator.py  # LLM-based quiz generation
├── data/                   # Raw source documents
│   └── README.md          # Document placement instructions
├── vectorstore/            # Persistent vector storage
│   └── README.md          # Vectorstore management
├── langsmith/              # LangSmith configuration
│   └── README.md          # Chain tracking setup
├── requirements.txt        # Python dependencies
├── .gitignore             # Git exclusions
└── README.md              # This file
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **RAG Framework**: LangChain v0.2+
- **Vector Database**: ChromaDB (local development)
- **Embeddings**: OpenAI Embeddings (with HuggingFace fallback)
- **LLM**: OpenAI GPT models / Groq (optional)
- **Monitoring**: LangSmith
- **Document Processing**: RecursiveCharacterTextSplitter
- **Token Management**: tiktoken

## 🚀 Local Development Setup

### Prerequisites
- Python 3.8+
- Git
- OpenAI API key
- LangSmith API key (optional)

### Step 1: Clone and Setup Virtual Environment

```bash
# Clone the repository
git clone https://github.com/onchainlabs1/ai-act.git
cd ai-act

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Environment Configuration

Create a `.env` file in the root directory:

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Groq API Key (for alternative LLM)
GROQ_API_KEY=gsk-your-groq-api-key-here

# Optional: LangSmith Configuration
LANGCHAIN_API_KEY=ls-your-langsmith-api-key-here
LANGCHAIN_PROJECT=ai-act-tutor
LANGCHAIN_TRACING_V2=true
```

### Step 4: Add Source Documents

Place the EU AI Act document (PDF or HTML) in the `data/` directory:

```bash
# Example: Copy your document to the data folder
cp /path/to/your/eu-ai-act.pdf data/
```

### Step 5: Initialize Vector Store (Optional)

If you want to populate the vector store with documents:

```bash
# Run the document loader (if implemented)
python -c "from core.loader import load_eu_ai_act; load_eu_ai_act('data/your-document.pdf')"
```

### Step 6: Run the Application

```bash
# Start the Streamlit app
streamlit run app/main.py
```

The application will be available at `http://localhost:8501`

## ☁️ Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

Ensure your project is pushed to GitHub with the correct structure:

```bash
# Verify your project structure
ls -la

# Should show: app/, core/, data/, vectorstore/, requirements.txt, etc.
```

### Step 2: Create Streamlit Configuration

Create `.streamlit/config.toml` file:

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Step 3: Configure Streamlit Cloud Secrets

In your Streamlit Cloud dashboard:

1. Go to your app settings
2. Navigate to "Secrets"
3. Add the following secrets:

```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
GROQ_API_KEY = "gsk-your-groq-api-key-here"
LANGCHAIN_API_KEY = "ls-your-langsmith-api-key-here"
LANGCHAIN_PROJECT = "ai-act-tutor"
LANGCHAIN_TRACING_V2 = "true"
```

### Step 4: Deploy

1. Connect your GitHub repository to Streamlit Cloud
2. Set the entrypoint to: `app/main.py`
3. Deploy the application

## 🔑 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key for embeddings and LLM | `sk-...` |

### Optional Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GROQ_API_KEY` | Alternative LLM provider | `gsk-...` |
| `LANGCHAIN_API_KEY` | LangSmith API key for monitoring | `ls-...` |
| `LANGCHAIN_PROJECT` | LangSmith project name | `ai-act-tutor` |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith tracing | `true` |

## 🔧 Development Tips

### Switching Between LLM Providers

If you implement `/app/settings.py`, you can switch between OpenAI and Groq:

```python
# In your settings page
llm_provider = st.selectbox(
    "Choose LLM Provider:",
    ["OpenAI", "Groq"],
    key="llm_provider"
)

# Update environment variables accordingly
if llm_provider == "Groq":
    os.environ["USE_GROQ"] = "true"
else:
    os.environ["USE_GROQ"] = "false"
```

### Security Best Practices

- **Never commit `.env` files** - They are already in `.gitignore`
- **Use Streamlit Secrets** for production deployments
- **Rotate API keys** regularly
- **Monitor usage** through LangSmith

### Performance Optimization

```bash
# For development, you can limit token usage
export OPENAI_MAX_TOKENS=1000

# Enable debug logging
export STREAMLIT_LOG_LEVEL=debug
```

### Vector Store Management

```bash
# Clear vector store (if needed)
rm -rf vectorstore/chroma/*

# Rebuild index
python -c "from core.loader import load_eu_ai_act; load_eu_ai_act('data/your-document.pdf')"
```

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Key Error**
```bash
Error: Invalid API key
```
**Solution**: Verify your API key in `.env` file and ensure it's valid.

**ChromaDB Connection Error**
```bash
Error: Unable to connect to vectorstore
```
**Solution**: Ensure `vectorstore/` directory exists and has write permissions.

**Streamlit Port Already in Use**
```bash
Error: Port 8501 is already in use
```
**Solution**: Use `streamlit run app/main.py --server.port 8502`

**Missing Dependencies**
```bash
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Activate virtual environment and run `pip install -r requirements.txt`

### Debug Mode

```bash
# Enable debug logging
export STREAMLIT_LOG_LEVEL=debug
streamlit run app/main.py

# Check environment variables
python -c "import os; print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

## 📊 Monitoring and Analytics

### LangSmith Integration

If you have LangSmith configured:

1. **View Chain Runs**: Monitor RAG chain performance
2. **Track Token Usage**: Monitor API costs
3. **Debug Issues**: Trace through chain execution
4. **Optimize Prompts**: A/B test different prompts

### Local Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🤝 Contributing

### Development Workflow

```bash
# Fork and clone
git clone https://github.com/your-username/ai-act.git
cd ai-act

# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... your code changes ...

# Test locally
streamlit run app/main.py

# Commit and push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# Create Pull Request
```

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints where appropriate
- Include docstrings for all functions
- Use meaningful variable and function names
- Test your changes locally before pushing

## 📝 TODO List

### High Priority
- [ ] Implement document loading (PDF/HTML)
- [ ] Complete RAG chain integration
- [ ] Add LangSmith tracking
- [ ] Implement chat interface functionality
- [ ] Add citation formatting

### Medium Priority
- [ ] Create study modules content
- [ ] Implement quiz generation
- [ ] Add progress tracking
- [ ] Optimize token usage
- [ ] Add error handling

### Low Priority
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Export functionality
- [ ] Mobile optimization
- [ ] Integration with other AI regulations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- European Union for the AI Act regulation
- LangChain team for the excellent RAG framework
- Streamlit for the intuitive web app framework
- OpenAI for the powerful language models

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

---

**Note**: This project is actively under development. Features and documentation will be updated regularly. 