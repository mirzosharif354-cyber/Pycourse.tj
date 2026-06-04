// MyCourse.tj — chat.js
const CSRF = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
let ROOM_SLUG = '';
let lastId = 0;

function initChat(slug, last) {
    ROOM_SLUG = slug;
    lastId = last;
    scrollToBottom();
    setInterval(pollMessages, 3000);
}

function scrollToBottom() {
    const area = document.getElementById('msgs-area');
    if (area) area.scrollTop = area.scrollHeight;
}

function appendMessage(msg, isMe) {
    const area = document.getElementById('msgs-area');
    const div = document.createElement('div');
    div.className = 'msg-group ' + (isMe ? 'me' : 'them');
    div.innerHTML = `<div class="msg-av">👤</div>
        <div class="msg-body">
            <div class="msg-name">${msg.user}</div>
            <div class="bubble">${msg.text}</div>
            <div class="msg-time">${msg.time}</div>
        </div>`;
    area.appendChild(div);
    scrollToBottom();
}

async function sendMessage() {
    const inp = document.getElementById('msg-input');
    const txt = inp.value.trim();
    if (!txt) return;
    try {
        const r = await fetch('/chat/api/send/', {
            method: 'POST',
            headers: {'X-CSRFToken': CSRF, 'Content-Type': 'application/json'},
            body: JSON.stringify({room: ROOM_SLUG, content: txt})
        });
        const d = await r.json();
        if (d.ok) {
            appendMessage(d.msg, true);
            lastId = d.msg.id;
            inp.value = '';
            inp.style.height = '';
            document.getElementById('emoji-picker').classList.remove('show');
        }
    } catch(e) {}
}

async function pollMessages() {
    try {
        const r = await fetch(`/chat/api/poll/${ROOM_SLUG}/?last=${lastId}`);
        const d = await r.json();
        d.msgs.forEach(m => {
            if (!m.me) { appendMessage(m, false); lastId = m.id; }
        });
    } catch(e) {}
}

function toggleEmoji() { document.getElementById('emoji-picker').classList.toggle('show'); }
function addEmoji(e) { const i = document.getElementById('msg-input'); i.value += e; i.focus(); }
