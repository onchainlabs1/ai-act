# AI Act Tutor

An interactive Streamlit-based educational tool for studying and exploring the European Union AI Act (Regulation 2024/1689) through Retrieval-Augmented Generation (RAG), interactive quizzes, and guided study modules.

## 🎯 Project Overview

AI Act Tutor is designed to help AI practitioners, lawyers, policy students, and anyone interested in understanding the EU AI Act through an intuitive, AI-powered interface. The application leverages state-of-the-art RAG technology to provide accurate, citation-backed responses about the regulation.

## 🚀 Key Features

### Current Features
- **Multi-page Streamlit Interface**: Clean, responsive UI with navigation between Chat, Study, and Quiz modules
- **Modular Architecture**: Well-organized codebase for easy maintenance and extensibility
- **RAG Pipeline**: LangChain v0.2+ based retrieval system with citation support
- **Local Vector Storage**: ChromaDB for efficient document retrieval and persistence

### Planned Features
- **Interactive Chat**: Real-time Q&A with the AI Act using RAG
- **Guided Study Modules**: Structured learning paths through the regulation
- **Dynamic Quiz Generation**: LLM-powered multiple-choice questions
- **Citation Tracking**: Always cite specific articles and sections
- **LangSmith Integration**: Chain monitoring and optimization
- **Multi-language Support**: Extensible for other jurisdictions

## 🏗️ Architecture

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
- **LLM**: OpenAI GPT models
- **Monitoring**: LangSmith
- **Document Processing**: RecursiveCharacterTextSplitter
- **Token Management**: tiktoken

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/onchainlabs1/ai-act.git
cd ai-act
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langsmith_api_key_here  # Optional
LANGCHAIN_PROJECT=ai-act-tutor  # Optional
```

### 4. Add Source Documents
Place the EU AI Act document (PDF or HTML) in the `data/` directory.

### 5. Run the Application
```bash
streamlit run app/main.py
```

The application will be available at `http://localhost:8501`

## 📚 Usage Guide

### Chat Interface
- Ask questions about the EU AI Act
- Receive citation-backed responses
- Explore specific articles and sections

### Study Modules
- Follow guided learning paths
- Interactive lessons and explanations
- Progress tracking (future feature)

### Quiz System
- Test your knowledge with generated questions
- Multiple-choice format
- Immediate feedback and explanations

## 🔧 Development

### Project Structure Guidelines

#### Adding New Features
1. **App Modules**: Add new pages in `app/` directory
2. **Core Logic**: Implement business logic in `core/` directory
3. **Data**: Place new documents in `data/` directory
4. **Configuration**: Update relevant config files

#### RAG Pipeline Customization
- Modify `core/rag_chain.py` for chain changes
- Update `core/loader.py` for document processing
- Adjust chunking parameters in loader.py

#### Vector Store Management
- ChromaDB files are stored in `vectorstore/`
- Rebuild index by deleting and re-running ingestion
- Monitor performance with LangSmith

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints where appropriate
- Include docstrings for all functions
- Use meaningful variable and function names

### Testing
```bash
# Run basic tests (when implemented)
python -m pytest tests/

# Check code style
flake8 app/ core/
```

## 🔒 Security Considerations

- **API Keys**: Never commit `.env` files or hardcode API keys
- **Document Access**: Ensure proper access controls for sensitive documents
- **Data Privacy**: Local vector storage for development
- **Input Validation**: Validate all user inputs

## 📊 Performance Optimization

### Token Efficiency
- Chunk size: 512 tokens with 64 token overlap
- Limit context window usage
- Optimize prompt templates
- Use streaming responses where appropriate

### Vector Store Optimization
- Regular index maintenance
- Monitor retrieval performance
- Optimize embedding dimensions
- Consider hybrid search strategies

## 🚀 Deployment

### Local Development
```bash
streamlit run app/main.py
```

### Production Considerations
- Use production-grade vector database (Pinecone, Weaviate)
- Implement proper authentication
- Set up monitoring and logging
- Configure CORS and security headers
- Use environment-specific configurations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Workflow
```bash
# Create and switch to feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature
```

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

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Key Error**
```
Error: Invalid API key
```
Solution: Check your `.env` file and ensure the API key is correct.

**ChromaDB Connection Error**
```
Error: Unable to connect to vectorstore
```
Solution: Ensure the `vectorstore/` directory exists and has write permissions.

**Streamlit Port Already in Use**
```
Error: Port 8501 is already in use
```
Solution: Use `streamlit run app/main.py --server.port 8502`

### Debug Mode
```bash
# Enable debug logging
export STREAMLIT_LOG_LEVEL=debug
streamlit run app/main.py
```

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