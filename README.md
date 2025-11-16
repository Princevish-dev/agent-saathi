# 🌟 Agent Saathi – Your Companion for Good

> *"Transforming discomfort into design-worthy comfort — helping users heal, grow, and create with soul."*

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ADK Concepts](https://img.shields.io/badge/ADK-10%2F15%20Concepts-green)](https://developers.google.com/assistant)

A modular, multi-agent system built with emotional intelligence that provides compassionate support, personalized study planning, and community impact through AI companionship.

## 🎯 Vision

Agent Saathi embodies the blueprint style of its creator Prince — modular, poetic, and emotionally resonant. It's not just an AI agent; it's a companion that walks with you through life's challenges and triumphs.

## 🏗️ Architecture
Agent Saathi System
├── 💭 Emotional Support Agent
├── 📚 Study Planning Agent
├── 🌍 Community Agent
└── 📱 Social Media Agent

### Core Features

- **🧠 Emotional Intelligence**: Validates and enhances emotional tone in all interactions
- **🔄 LoopAgent Pattern**: Retry mechanisms for reliable responses
- **📚 Memory Management**: Long-term emotional pattern storage with auto-compaction
- **🔗 A2A Protocol**: Seamless inter-agent communication
- **👁️ Observability**: Comprehensive logging and performance tracking
- **🎯 Context Engineering**: Smart memory optimization

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
4. **Configure environment**
   # Create .env file with your API key
   echo GOOGLE_API_KEY=your_actual_api_key_here > .env
5. **Run the system**
   python -m blogger_agent.main
