# 🌟 Agent Saathi – Your Companion for Good

> *"Transforming discomfort into design-worthy comfort — helping users heal, grow, and create with soul."*

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ADK Concepts](https://img.shields.io/badge/ADK-15%2F15%20Concepts-green)](https://developers.google.com/assistant)
[![Hackathon](https://img.shields.io/badge/Kaggle-Google%20AI%20Agents%20Hackathon%202025-orange)](https://kaggle.com)

A comprehensive multi-agent system implementing **all 15 ADK concepts** that provides compassionate emotional support, personalized study planning, and community impact through advanced AI companionship.

## 🎯 Vision

Agent Saathi embodies the blueprint style of its creator Prince — modular, poetic, and emotionally resonant. It's not just an AI agent; it's a companion that walks with you through life's challenges and triumphs.

## 🏗️ Architecture
Agent Saathi System
├── 💭 Emotional Support Agent (LoopAgent + Memory)
├── 📚 Study Planning Agent (Personalized scheduling)
├── 🌍 Community Agent (Social impact focus)
└── 📱 Social Media Agent (Storytelling & outreach)

### 🎯 All 15 ADK Concepts Implemented

**🤖 Multi-agent System**
- ✅ Agent powered by LLM (Gemini AI integration)
- ✅ Sequential agents (Emotional → Study workflow) 
- ✅ Parallel agents (Concurrent execution)
- ✅ Loop agents (EmotionalLoopAgent with retry)

**🛠️ Tools & Integration**
- ✅ MCP Tools (Model Context Protocol)
- ✅ Custom tools (FileTools, AnalysisTools, SocialTools)
- ✅ Built-in tools (Google Gemini AI)
- ✅ OpenAPI tools (External API integration)

**🧠 Advanced Features**
- ✅ Long-running operations (Pause/Resume capability)
- ✅ Sessions & Memory (State management)
- ✅ Long term memory (EmotionalMemoryBank)
- ✅ Context engineering (Auto memory compaction)
- ✅ Observability (Logging, Tracing, Metrics)
- ✅ Agent evaluation (Performance metrics)
- ✅ A2A Protocol (Inter-agent communication)
- ✅ Agent deployment (Professional packaging)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google API Key ([Get free API key](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Princevish-dev/agent-saathi.git
   cd agent-saathi
2. **Set up environment**
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On Linux/Mac:
   source venv/bin/activate
3. **Install dependencies**
   pip install -r requirements.txt
4. **Configure environmen**
   python -m blogger_agent.main