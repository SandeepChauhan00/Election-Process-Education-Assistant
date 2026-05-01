/**
 * ============================================
 * ELECTION EDUCATION ASSISTANT - JavaScript
 * Premium interactive chat application
 * ============================================
 */

// Configure marked.js for markdown rendering
marked.setOptions({
    breaks: true,
    gfm: true,
    headerIds: false,
    mangle: false
});

// ============================================
// THEME MANAGEMENT
// ============================================

function toggleTheme() {
    const body = document.body;
    const btn = document.getElementById('themeToggle');
    const isDark = body.getAttribute('data-theme') === 'dark';

    if (isDark) {
        body.removeAttribute('data-theme');
        btn.innerHTML = '<i class="fas fa-moon"></i>';
        localStorage.setItem('theme', 'light');
    } else {
        body.setAttribute('data-theme', 'dark');
        btn.innerHTML = '<i class="fas fa-sun"></i>';
        localStorage.setItem('theme', 'dark');
    }
}

function loadTheme() {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        const btn = document.getElementById('themeToggle');
        if (btn) btn.innerHTML = '<i class="fas fa-sun"></i>';
    }
}

// ============================================
// ANIMATED BACKGROUND PARTICLES
// ============================================

function createParticles() {
    const container = document.getElementById('bgParticles');
    if (!container) return;

    const colors = ['#FF9933', '#138808', '#2563eb', '#4f46e5'];

    for (let i = 0; i < 15; i++) {
        const particle = document.createElement('div');
        particle.className = 'bg-particle';
        const size = Math.random() * 80 + 20;
        const color = colors[Math.floor(Math.random() * colors.length)];

        particle.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            background: ${color};
            left: ${Math.random() * 100}%;
            animation-duration: ${Math.random() * 25 + 15}s;
            animation-delay: ${Math.random() * 10}s;
        `;
        container.appendChild(particle);
    }
}

// ============================================
// SIDEBAR (Mobile)
// ============================================

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
}

// ============================================
// CORE CHAT FUNCTIONS
// ============================================

async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();

    if (!message) return;

    // Clear input
    input.value = '';
    input.style.height = 'auto';

    // Add user message
    addMessage(message, 'user');

    // Show typing indicator
    const typingId = showTypingIndicator();

    // Disable send button
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        removeTypingIndicator(typingId);

        if (data.error) {
            addMessage('❌ ' + (data.error || 'Sorry, an error occurred. Please try again.'), 'bot');
        } else {
            addMessage(data.response, 'bot');
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('❌ Connection error. Please check your internet and try again.', 'bot');
        console.error('Chat error:', error);
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

async function loadTopic(topicId) {
    showToast('Loading topic...');

    // Disable topic buttons
    const topicBtns = document.querySelectorAll('.topic-btn');
    topicBtns.forEach(btn => btn.disabled = true);

    const typingId = showTypingIndicator();

    // Close sidebar on mobile
    const sidebar = document.getElementById('sidebar');
    if (sidebar.classList.contains('open')) {
        toggleSidebar();
    }

    try {
        const response = await fetch('/topic/' + topicId);
        const data = await response.json();
        removeTypingIndicator(typingId);

        if (data.error) {
            addMessage('❌ Error loading topic. Please try again.', 'bot');
        } else {
            addMessage(data.response, 'bot');
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('❌ Connection error. Please try again.', 'bot');
    } finally {
        topicBtns.forEach(btn => btn.disabled = false);
    }
}

function sendQuickQuestion(question) {
    const input = document.getElementById('userInput');
    input.value = question;
    sendMessage();
}

async function clearChat() {
    if (!confirm('Clear chat history and start fresh?')) return;

    try {
        await fetch('/clear', { method: 'POST' });
    } catch (e) {
        console.error('Clear error:', e);
    }

    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '';
    addWelcomeMessage();
    showToast('Chat cleared! Ready for a fresh start 🗳️');
}

// ============================================
// UI HELPER FUNCTIONS
// ============================================

function addMessage(content, role) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    const time = new Date().toLocaleTimeString('en-IN', {
        hour: '2-digit', minute: '2-digit'
    });

    if (role === 'user') {
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML =
            '<div class="message-content">' +
                '<div class="message-bubble">' + escapeHtml(content) + '</div>' +
                '<div class="message-time">' + time + '</div>' +
            '</div>' +
            '<div class="message-avatar">👤</div>';
    } else {
        messageDiv.className = 'message bot-message';
        var renderedContent = marked.parse(content);
        messageDiv.innerHTML =
            '<div class="message-avatar">🗳️</div>' +
            '<div class="message-content">' +
                '<div class="message-bubble">' + renderedContent + '</div>' +
                '<div class="message-time">' + time + '</div>' +
            '</div>';
    }

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addWelcomeMessage() {
    var chatMessages = document.getElementById('chatMessages');
    var welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'message bot-message welcome-message';
    welcomeDiv.id = 'welcomeMessage';
    welcomeDiv.innerHTML =
        '<div class="message-avatar">🗳️</div>' +
        '<div class="message-content">' +
            '<div class="message-bubble welcome-bubble">' +
                '<h3>👋 Welcome back to ElectionBot!</h3>' +
                '<p>Ready to learn about elections? Choose a topic or ask me anything!</p>' +
                '<div class="welcome-divider"><span>🎯 Quick Start</span></div>' +
                '<div class="quick-start-grid">' +
                    '<button class="quick-start-btn" onclick="sendQuickQuestion(\'Explain the complete Indian election process\')">' +
                        '<span class="qs-icon">📚</span><span class="qs-text">Election Process</span>' +
                    '</button>' +
                    '<button class="quick-start-btn" onclick="sendQuickQuestion(\'How do I register as a voter?\')">' +
                        '<span class="qs-icon">📝</span><span class="qs-text">Register to Vote</span>' +
                    '</button>' +
                    '<button class="quick-start-btn" onclick="sendQuickQuestion(\'How does voting work on election day?\')">' +
                        '<span class="qs-icon">🗳️</span><span class="qs-text">How to Vote</span>' +
                    '</button>' +
                    '<button class="quick-start-btn" onclick="sendQuickQuestion(\'Give me an election quiz\')">' +
                        '<span class="qs-icon">🎯</span><span class="qs-text">Take a Quiz</span>' +
                    '</button>' +
                '</div>' +
            '</div>' +
            '<div class="message-time">Just now</div>' +
        '</div>';
    chatMessages.appendChild(welcomeDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    var chatMessages = document.getElementById('chatMessages');
    var typingDiv = document.createElement('div');
    var id = 'typing-' + Date.now();
    typingDiv.id = id;
    typingDiv.className = 'message bot-message';
    typingDiv.innerHTML =
        '<div class="message-avatar">🗳️</div>' +
        '<div class="message-content">' +
            '<div class="typing-indicator">' +
                '<div class="typing-dot"></div>' +
                '<div class="typing-dot"></div>' +
                '<div class="typing-dot"></div>' +
            '</div>' +
        '</div>';
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
    return id;
}

function removeTypingIndicator(id) {
    var elem = document.getElementById(id);
    if (elem) elem.remove();
}

function scrollToBottom() {
    var chatMessages = document.getElementById('chatMessages');
    requestAnimationFrame(function() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
}

function escapeHtml(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

function showToast(message, duration) {
    duration = duration || 3000;
    var toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(function() { toast.classList.remove('show'); }, duration);
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Load saved theme
    loadTheme();

    // Create animated background particles
    createParticles();

    // Focus on input
    var input = document.getElementById('userInput');
    if (input) input.focus();

    console.log('🗳️ ElectionBot initialized successfully!');
    console.log('Built for PromptWars: Virtual Challenge 2');
    console.log('Powered by Google Gemini AI');
});
