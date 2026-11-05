/**
 * script.js - Lógica interativa do Chat para o Microsoft Foundry
 */

document.addEventListener('DOMContentLoaded', () => {
    // Determina a URL base da API (se aberto diretamente ou via Live Server)
    const isServedByBackend = window.location.protocol.startsWith('http') && 
                              (window.location.port === '5000' || window.location.port === '');
    const API_BASE_URL = isServedByBackend ? '' : 'http://127.0.0.1:5000';

    // Elementos do DOM
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicator = document.getElementById('typing-indicator');
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    const modelBadge = document.getElementById('model-badge');
    const clearBtn = document.getElementById('clear-btn');

    // Histórico da sessão atual
    let conversationHistory = [];
    let isSending = false;

    // =========================================================================
    // 1. Verificação de Status do Servidor
    // =========================================================================
    async function checkServerStatus() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/status`);
            if (!response.ok) throw new Error('Servidor retornou erro');
            const data = await response.json();

            statusIndicator.className = 'status-indicator online';
            statusText.textContent = 'Conectado';
            if (data.model) {
                modelBadge.textContent = data.model;
            }
        } catch (error) {
            console.warn('Backend não disponível no momento:', error);
            statusIndicator.className = 'status-indicator offline';
            statusText.textContent = 'Backend Desconectado';
        }
    }

    // =========================================================================
    // 2. Formatação e Utilitários
    // =========================================================================
    function getFormattedTime() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function formatMarkdown(text) {
        // Escapa tags perigosas
        let safe = escapeHtml(text);

        // Bloco de código: ```linguagem\nconteudo```
        safe = safe.replace(/```([\s\S]*?)```/g, (match, p1) => {
            return `<pre><code>${p1.trim()}</code></pre>`;
        });

        // Código inline: `codigo`
        safe = safe.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Negrito: **texto**
        safe = safe.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Quebras de linha
        safe = safe.replace(/\n/g, '<br>');

        return safe;
    }

    function scrollToBottom() {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }

    // =========================================================================
    // 3. Renderização de Mensagens
    // =========================================================================
    function appendMessage(role, content, isError = false) {
        const messageDiv = document.createElement('div');
        const messageClass = role === 'user' ? 'user-message' : 'assistant-message';
        messageDiv.className = `message ${messageClass} ${isError ? 'error-message' : ''}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        if (isError) {
            contentDiv.innerHTML = `⚠️ <strong>Atenção:</strong> ${formatMarkdown(content)}`;
        } else if (role === 'user') {
            contentDiv.textContent = content; // Para usuário, texto puro seguro
        } else {
            contentDiv.innerHTML = formatMarkdown(content);
        }

        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = getFormattedTime();

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeSpan);
        chatMessages.appendChild(messageDiv);

        scrollToBottom();
    }

    // =========================================================================
    // 4. Envio de Mensagem para o Backend
    // =========================================================================
    async function sendMessage(text) {
        if (!text || !text.trim() || isSending) return;

        const cleanText = text.trim();
        isSending = true;

        // Adiciona a mensagem do usuário na tela e no histórico local
        appendMessage('user', cleanText);
        conversationHistory.push({ role: 'user', content: cleanText });

        // Limpa e reseta o campo de texto
        userInput.value = '';
        autoResizeTextarea();
        userInput.disabled = true;
        sendButton.disabled = true;

        // Exibe indicador de digitação
        typingIndicator.classList.add('active');
        scrollToBottom();

        try {
            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: cleanText,
                    history: conversationHistory
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                const replyText = data.reply || 'Sem resposta do agente.';
                appendMessage('assistant', replyText);
                conversationHistory.push({ role: 'assistant', content: replyText });
            } else {
                const errorMsg = data.error || 'Ocorreu um erro ao processar sua pergunta.';
                appendMessage('assistant', errorMsg, true);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            appendMessage(
                'assistant',
                'Não foi possível conectar ao servidor backend (http://127.0.0.1:5000). Certifique-se de que o backend está em execução com "python run.py".',
                true
            );
        } finally {
            isSending = false;
            typingIndicator.classList.remove('active');
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    // =========================================================================
    // 5. Ajuste Dinâmico da Altura do Textarea
    // =========================================================================
    function autoResizeTextarea() {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
    }

    userInput.addEventListener('input', autoResizeTextarea);

    // =========================================================================
    // 6. Atalhos de Teclado e Eventos do Formulário
    // =========================================================================
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        sendMessage(userInput.value);
    });

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Clique nas sugestões rápidas
    document.addEventListener('click', (e) => {
        const chip = e.target.closest('.chip-btn');
        if (chip) {
            const prompt = chip.getAttribute('data-prompt');
            if (prompt) {
                sendMessage(prompt);
            }
        }
    });

    // Limpar conversa
    clearBtn.addEventListener('click', () => {
        if (confirm('Deseja realmente limpar a conversa atual?')) {
            conversationHistory = [];
            // Remove mensagens exceto o primeiro card de boas-vindas
            const messages = chatMessages.querySelectorAll('.message');
            messages.forEach((msg, index) => {
                if (index > 0) msg.remove();
            });
            userInput.focus();
        }
    });

    // Inicialização
    checkServerStatus();
    userInput.focus();
});

