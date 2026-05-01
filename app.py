"""
🗳️ Election Process Education Assistant
========================================
An AI-powered interactive assistant for learning about India's election process.
Built with Google Gemini AI and Flask for PromptWars: Virtual Challenge 2.

Author: Sandeep Kumar
License: MIT
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, session
from google import genai
from google.genai import types
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "election-edu-secret-2024")

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
    logger.info("✅ Gemini API client configured successfully")
else:
    logger.warning("⚠️ GEMINI_API_KEY not set. Chat functionality will be limited.")

# Model name
MODEL_NAME = "gemini-2.0-flash"

# System instruction for the Election Education Bot
SYSTEM_INSTRUCTION = """
You are ElectionBot - an expert, friendly, and interactive Election Process 
Education Assistant. Your role is to help users understand:

1. ELECTION PROCESSES in India (General Elections, State Elections, Local Body Elections)
2. ELECTION TIMELINES - Step by step from announcement to results
3. VOTER REGISTRATION - How to register, check registration, voter ID
4. CANDIDATE FILING - Nomination process, eligibility criteria
5. ELECTION COMMISSION - Role of ECI, Model Code of Conduct
6. VOTING PROCESS - How to vote, EVM machines, VVPAT
7. COUNTING & RESULTS - How votes are counted, declared
8. ELECTORAL ROLLS - How to check, update voter list
9. ELECTION LAWS - Key laws governing elections in India
10. COMPARATIVE ELECTIONS - Different election types (FPTP, PR systems)

IMPORTANT RULES:
- Always be NON-PARTISAN and NEUTRAL
- Never support or oppose any political party or candidate
- Provide FACTUAL, ACCURATE information only
- Use SIMPLE language with emojis for better understanding
- Break complex processes into NUMBERED STEPS
- Provide INTERACTIVE quizzes when asked
- Include REAL DATES and TIMELINES when known
- If asked about specific election dates, note they change each election
- Always encourage CIVIC PARTICIPATION and VOTING

FORMAT GUIDELINES:
- Use bullet points and numbered lists
- Use emojis to make content engaging
- Bold important terms using **term**
- Provide examples from real Indian elections
- Suggest related topics the user might want to explore
- Use markdown headers (##, ###) for organized sections
- Include tables where comparisons help understanding

Start conversations warmly and ask what aspect of elections 
they want to learn about.
"""

# Election topics for quick access
ELECTION_TOPICS = [
    {"id": "voter_registration", "title": "📝 Voter Registration",
     "description": "How to register as a voter", "icon": "📝"},
    {"id": "election_timeline", "title": "📅 Election Timeline",
     "description": "Complete election process timeline", "icon": "📅"},
    {"id": "voting_process", "title": "🗳️ How to Vote",
     "description": "Step-by-step voting guide", "icon": "🗳️"},
    {"id": "election_commission", "title": "⚖️ Election Commission",
     "description": "Role of ECI in elections", "icon": "⚖️"},
    {"id": "candidate_filing", "title": "👤 Candidate Filing",
     "description": "How candidates file nominations", "icon": "👤"},
    {"id": "counting_results", "title": "📊 Vote Counting",
     "description": "How votes are counted and results declared", "icon": "📊"},
    {"id": "model_code", "title": "📋 Model Code of Conduct",
     "description": "Rules during election period", "icon": "📋"},
    {"id": "evm_vvpat", "title": "🖥️ EVM & VVPAT",
     "description": "Electronic voting machines explained", "icon": "🖥️"},
    {"id": "election_types", "title": "🏛️ Types of Elections",
     "description": "Different elections in India", "icon": "🏛️"},
    {"id": "quiz", "title": "🎯 Election Quiz",
     "description": "Test your election knowledge", "icon": "🎯"}
]

# Pre-defined quick questions
QUICK_QUESTIONS = [
    "What is the complete timeline of Indian General Elections?",
    "How do I register as a voter in India?",
    "How does the EVM voting machine work?",
    "What is the Model Code of Conduct?",
    "How are election results counted and declared?",
    "What are the eligibility criteria to vote in India?",
    "How does the nomination process work for candidates?",
    "What is the role of Election Commission of India?",
    "Give me a quiz on Indian elections",
    "Explain FPTP vs Proportional Representation"
]

# Topic-specific detailed prompts
TOPIC_PROMPTS = {
    "voter_registration": (
        "Explain the complete voter registration process in India step by step. "
        "Include online and offline methods, required documents, Form 6, "
        "how to check registration status on NVSP portal, and age eligibility."
    ),
    "election_timeline": (
        "Give me a detailed timeline of the complete Indian General Election process "
        "from announcement to result declaration. Include all major steps with typical duration."
    ),
    "voting_process": (
        "Explain the complete voting process in India step by step. From entering "
        "the polling booth to casting vote using EVM. Include identity verification, "
        "ink mark, ballot unit operation, and VVPAT slip."
    ),
    "election_commission": (
        "Explain the role and powers of the Election Commission of India. "
        "Cover its constitutional provisions (Article 324), composition, appointment, "
        "powers before/during/after elections, and landmark decisions."
    ),
    "candidate_filing": (
        "Explain the complete process of filing nomination for elections in India. "
        "Include eligibility criteria, required documents, security deposit amounts, "
        "scrutiny process, and withdrawal timeline."
    ),
    "counting_results": (
        "Explain the complete vote counting and result declaration process in India. "
        "Include how EVM votes are counted, VVPAT verification, postal ballots, "
        "how winners are declared, and the role of Returning Officer."
    ),
    "model_code": (
        "Explain the Model Code of Conduct in Indian elections. What is it, "
        "when does it apply, what are the key sections, how is it enforced, "
        "and give examples of MCC violations."
    ),
    "evm_vvpat": (
        "Explain how EVM and VVPAT work in Indian elections. "
        "Cover the 3 units, security features, mock polls, and address common "
        "concerns about EVM security with facts."
    ),
    "election_types": (
        "Explain all types of elections in India: "
        "Lok Sabha, Rajya Sabha, State Vidhan Sabha, Panchayat, Municipal. "
        "Compare their frequency, voting method, and significance."
    ),
    "quiz": (
        "Give me an interactive quiz with 5 multiple-choice questions about "
        "Indian elections. Present one question with 4 options. "
        "Wait for my answer before revealing the correct answer."
    )
}


def get_or_create_chat_session():
    """Get existing chat history or create new session."""
    if 'chat_history' not in session:
        session['chat_history'] = []
    return session['chat_history']


def build_gemini_contents(chat_history):
    """Build contents list for Gemini API from chat history."""
    contents = []
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )
    return contents


def sanitize_input(text, max_length=2000):
    """Sanitize user input for security."""
    if not isinstance(text, str):
        return ""
    return text.strip()[:max_length]


# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    """Main page - renders the chat interface."""
    session.clear()
    logger.info("New session started")
    return render_template(
        'index.html',
        topics=ELECTION_TOPICS,
        quick_questions=QUICK_QUESTIONS
    )


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with Gemini AI."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request format'}), 400

        user_message = sanitize_input(data.get('message', ''))

        if not user_message:
            return jsonify({'error': 'Empty message'}), 400

        if not client:
            return jsonify({
                'error': 'AI model not configured. Please set GEMINI_API_KEY.'
            }), 503

        # Get chat history
        chat_history = get_or_create_chat_session()

        # Build contents with history + new message
        contents = build_gemini_contents(chat_history)
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)]
            )
        )

        # Generate response
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_output_tokens=4096,
            )
        )

        bot_response = response.text
        current_time = datetime.now().strftime("%H:%M")

        # Update session history
        chat_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": current_time
        })
        chat_history.append({
            "role": "model",
            "content": bot_response,
            "timestamp": current_time
        })

        # Keep only last 20 messages to manage token limits
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]

        session['chat_history'] = chat_history
        session.modified = True

        logger.info(f"Chat response generated ({len(bot_response)} chars)")

        return jsonify({
            'response': bot_response,
            'timestamp': current_time
        })

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({
            'error': 'Sorry, I encountered an error. Please try again.',
            'details': str(e)
        }), 500


@app.route('/topic/<topic_id>', methods=['GET'])
def get_topic(topic_id):
    """Get detailed information about a specific election topic."""
    prompt = TOPIC_PROMPTS.get(topic_id)
    if not prompt:
        return jsonify({'error': 'Topic not found'}), 404

    if not client:
        return jsonify({
            'error': 'AI model not configured. Please set GEMINI_API_KEY.'
        }), 503

    try:
        # Clear previous chat for fresh topic context
        session['chat_history'] = []

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            )
        ]

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_output_tokens=4096,
            )
        )

        bot_response = response.text
        current_time = datetime.now().strftime("%H:%M")

        # Save to session for follow-up questions
        chat_history = [
            {"role": "user", "content": prompt, "timestamp": current_time},
            {"role": "model", "content": bot_response, "timestamp": current_time}
        ]

        session['chat_history'] = chat_history
        session.modified = True

        logger.info(f"Topic '{topic_id}' loaded successfully")

        return jsonify({
            'response': bot_response,
            'timestamp': current_time
        })

    except Exception as e:
        logger.error(f"Topic error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear chat history and start fresh."""
    session.clear()
    logger.info("Chat session cleared")
    return jsonify({'status': 'cleared'})


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Cloud Run."""
    return jsonify({
        'status': 'healthy',
        'service': 'Election Education Assistant',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'gemini_configured': GEMINI_API_KEY is not None
    })


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    logger.error(f"Server error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    logger.info(f"🗳️ Election Education Assistant starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
