// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const messageInput = document.getElementById('messageInput');
const cityInput = document.getElementById('cityInput');
const sendBtn = document.getElementById('sendBtn');
const messagesContainer = document.getElementById('messagesContainer');

// Set example question
function setExample(question, city) {
    messageInput.value = question;
    if (city) {
        cityInput.value = city;
    }
    messageInput.focus();
}

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Add message to chat
function addMessage(content, isUser = false, toolUsed = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
    
    if (!isUser && toolUsed) {
        // Auto-detect tool based on content if toolUsed is not provided or incorrect
        let detectedTool = toolUsed;
        if (!detectedTool) {
            detectedTool = detectToolFromContent(content);
        }
        
        const toolName = getToolName(detectedTool);
        const toolIcon = getToolIcon(detectedTool);
        messageDiv.innerHTML = `
            <div class="tool-indicator">
                <i class="fas ${toolIcon} tool-icon"></i>
                ${toolName}
            </div>
            ${formatResponse(content)}
        `;
    } else {
        messageDiv.textContent = content;
    }
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Auto-detect tool from content (fallback mechanism)
function detectToolFromContent(content) {
    const lowerContent = content.toLowerCase();
    
    // Check for weather indicators
    if (lowerContent.includes('weather') || 
        lowerContent.includes('temperature') || 
        lowerContent.includes('°c') || 
        lowerContent.includes('°f') ||
        lowerContent.includes('humidity') ||
        lowerContent.includes('condition:') ||
        /temperature:\s*\d+\.?\d*\s*°[cf]/i.test(content)) {
        return 'weather';
    }
    
    // Check for dictionary indicators
    if (lowerContent.includes('definition') || 
        lowerContent.includes('meaning') || 
        lowerContent.includes('means') ||
        lowerContent.includes('defined as') ||
        /"([^"]+)"\s+(means|is)/i.test(content)) {
        return 'dictionary';
    }
    
    // Check for web search indicators
    if (lowerContent.includes('search') || 
        lowerContent.includes('found') || 
        lowerContent.includes('according to') ||
        lowerContent.includes('source') ||
        lowerContent.includes('information about')) {
        return 'web_search';
    }
    
    return 'assistant';
}

// Show loading indicator
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant-message';
    loadingDiv.id = 'loadingMessage';
    loadingDiv.innerHTML = `
        <div class="tool-indicator">
            <i class="fas fa-cog tool-icon"></i>
            Thinking...
        </div>
        <div class="loading">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
    `;
    messagesContainer.appendChild(loadingDiv);
    scrollToBottom();
}

// Hide loading indicator
function hideLoading() {
    const loadingMsg = document.getElementById('loadingMessage');
    if (loadingMsg) {
        loadingMsg.remove();
    }
}

// Get tool name for display (with more flexible matching)
function getToolName(tool) {
    // Handle various possible tool names from backend
    const toolName = String(tool).toLowerCase();
    
    if (toolName.includes('weather') || toolName === 'get_weather') {
        return 'Weather Information';
    } else if (toolName.includes('dictionary') || toolName.includes('define') || toolName === 'define_word') {
        return 'Dictionary Lookup';
    } else if (toolName.includes('search') || toolName === 'web_search') {
        return 'Web Search Results';
    } else if (toolName.includes('assistant') || toolName === 'assistant') {
        return 'Travel Assistant';
    }
    
    return 'Travel Assistant';
}

// Get tool icon (with more flexible matching)
function getToolIcon(tool) {
    // Handle various possible tool names from backend
    const toolName = String(tool).toLowerCase();
    
    if (toolName.includes('weather') || toolName === 'get_weather') {
        return 'fa-cloud-sun';
    } else if (toolName.includes('dictionary') || toolName.includes('define') || toolName === 'define_word') {
        return 'fa-book';
    } else if (toolName.includes('search') || toolName === 'web_search') {
        return 'fa-search';
    }
    
    return 'fa-robot';
}

// Scroll to bottom of messages
function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Format response with line breaks and preserve formatting
function formatResponse(text) {
    // Convert markdown-style bullet points to HTML
    let formattedText = text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^- (.*?)(?=<br>|$)/gm, '• $1');
    
    return formattedText;
}

// Send message to API
async function sendMessage() {
    const question = messageInput.value.trim();
    const city = cityInput.value.trim();
    
    if (!question) {
        alert('Please enter a question');
        return;
    }
    
    // Add user message
    addMessage(question, true);
    
    // Clear input (keep city if user wants to ask multiple questions about same city)
    messageInput.value = '';
    
    // Disable send button
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing';
    
    // Show loading
    showLoading();
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/assist`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                city: city || null
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove loading
        hideLoading();
        
        // Add assistant response
        if (data.success) {
            // Debug log to see what backend returns
            console.log('Backend response:', {
                answer: data.answer?.substring(0, 100) + '...',
                tool_used: data.tool_used,
                raw_tool_used: data.tool_used
            });
            
            addMessage(data.answer, false, data.tool_used);
        } else {
            addMessage("Sorry, I couldn't process your request. Please try again.", false);
        }
        
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        addMessage(`Sorry, there was an error connecting to the server. Please make sure the backend is running on ${API_BASE_URL}`, false);
    } finally {
        // Re-enable send button
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send';
        
        // Focus back on input
        messageInput.focus();
    }
}

// Check API health on load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (response.ok) {
            console.log('API is connected and healthy');
            // Optional: show a success message
            setTimeout(() => {
                const healthMsg = document.createElement('div');
                healthMsg.className = 'message assistant-message';
                healthMsg.style.fontSize = '0.9rem';
                healthMsg.style.opacity = '0.8';
                healthMsg.innerHTML = '<div class="tool-indicator"><i class="fas fa-check tool-icon"></i> System</div>✓ Connected to backend API';
                messagesContainer.appendChild(healthMsg);
                scrollToBottom();
            }, 500);
        }
    } catch (error) {
        console.warn('Could not connect to API. Make sure the backend is running on port 8000.');
        addMessage("⚠️ <strong>Note:</strong> Backend API is not connected. Please make sure the server is running on http://localhost:8000", false);
    }
}

// Initialize
window.onload = function() {
    messageInput.focus();
    checkAPIHealth();
    
    // Add event listener for city input
    cityInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            messageInput.focus();
        }
    });
};