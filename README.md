# CivicBot: Urban Planning Feedback Assistant

Overview:
CivicBot is an AI-powered assistant designed to help urban planners, city officials, and civic bodies retrieve insights from zoning regulations, environmental reports, park blueprints, and public feedback documents. It leverages RAG (Retrieval-Augmented Generation) and Groq’s LLM API to respond to policy, planning, and compliance queries in real-time.

Use Case Objective-
Enable city officials and planning teams to:
Ask questions about zoning, infrastructure plans, or community feedback.
Automatically reference internal planning documents.
Reduce time spent searching across reports and regulation files.

Tech Stack:
LLM API: Groq
Framework: Streamlit
RAG Engine: Custom vector search using cosine_similarity
Embedding Logic: Custom embedding pipeline
File Monitoring: watchdog for real-time document ingestion

Folder Structure: 
CIVICBOT/
│
├── config/                         
│   └── config.py                   
│
├── data/                            
│   ├── community_feedback_summary.txt
│   ├── environmental_impact_assessment.txt
│   ├── landscaping_plan.txt
│   ├── park_blueprint_summary.txt
│   └── zoning_regulation_excerpt.txt
│
├── models/                          
│   ├── embeddings.py              
│   └── llm.py                     
│
├── utils/                           
│   ├── logger.py                 
│   ├── prompt_engineering.py   
│   ├── rag_utils.py              
│   ├── response_modes.py         
│   └── web_search.py             
│
├── app.py                         
├── .env                            
├── requirements.txt                                  
