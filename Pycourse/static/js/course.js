// MyCourse.tj — course.js
const CSRF = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

function showPanel(name, btn) {
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.getElementById('panel-' + name).classList.add('active');
    document.querySelectorAll('.sb-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    const titles = {videos:'🎬 Видеодарсҳо', topics:'📚 Мавзуъҳо', tests:'📝 Тестҳо', tasks:'💻 Вазифаҳо'};
    const el = document.getElementById('panel-title');
    if (el) el.textContent = titles[name] || name;
}

let currentVideoId = null;

function openVideo(id, title, desc, url) {
    currentVideoId = id;
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-desc').textContent = desc;
    const pl = document.getElementById('video-player');
    if (url) {
        pl.innerHTML = `<iframe src="${url}" width="100%" height="100%" style="border:none;border-radius:10px;" allowfullscreen></iframe>`;
    } else {
        pl.innerHTML = '<span style="font-size:30px">🎬</span><span>Видео серверда мавҷуд аст</span>';
    }
    document.getElementById('video-modal').classList.add('open');
}

function closeModal() {
    document.getElementById('video-modal').classList.remove('open');
    document.getElementById('video-player').innerHTML = '';
}

async function markWatched() {
    if (!currentVideoId) return;
    const btn = document.getElementById('watch-btn');
    btn.disabled = true; btn.textContent = '⏳...';
    try {
        const r = await fetch(`/api/video/${currentVideoId}/watched/`, {
            method: 'POST', headers: {'X-CSRFToken': CSRF, 'Content-Type': 'application/json'}
        });
        const d = await r.json();
        if (d.ok) { btn.textContent = '✅ Тамомшуд!'; setTimeout(() => location.reload(), 700); }
    } catch(e) { btn.disabled = false; btn.textContent = '✅ Тамомшуд'; }
}

async function submitTest(testId, answer, btn) {
    const card = document.getElementById('tc' + testId);
    card.querySelectorAll('.opt-btn').forEach(b => b.disabled = true);
    const r = await fetch(`/api/test/${testId}/submit/`, {
        method: 'POST',
        headers: {'X-CSRFToken': CSRF, 'Content-Type': 'application/json'},
        body: JSON.stringify({answer})
    });
    const d = await r.json();
    const tr = document.getElementById('tr' + testId);
    if (d.correct) {
        btn.classList.add('ok');
        tr.className = 'test-result badge-g'; tr.style.display = 'block'; tr.textContent = '✅ Дуруст!';
    } else {
        btn.classList.add('no');
        tr.className = 'test-result badge-r'; tr.style.display = 'block'; tr.textContent = '❌ Нодуруст.';
        const opts = card.querySelectorAll('.opt-btn');
        const map = ['a','b','c','d'];
        opts.forEach((b, i) => { if (map[i] === d.correct_answer) b.classList.add('ok'); });
    }
}

async function submitTask(taskId) {
    const code = document.getElementById('cd' + taskId).value.trim();
    const msg  = document.getElementById('tm' + taskId);
    if (!code) { msg.className = 'task-msg'; msg.style.color = '#c62828'; msg.textContent = '⚠️ Код холӣ аст!'; return; }
    const r = await fetch(`/api/task/${taskId}/submit/`, {
        method: 'POST',
        headers: {'X-CSRFToken': CSRF, 'Content-Type': 'application/json'},
        body: JSON.stringify({code})
    });
    const d = await r.json();
    if (d.ok) { msg.style.color = '#2e7d4f'; msg.textContent = '✅ Фиристода шуд! Устод санҷиш мекунад.'; }
    else { msg.style.color = '#c62828'; msg.textContent = '⚠️ ' + d.msg; }
}
