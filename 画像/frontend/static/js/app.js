/**
 * 学生画像系统前端逻辑
 * 2026春季班全阶段科创编程课程体系
 */

// ========== 路径配置 ==========
const PATH_CONFIG = {
    // 幼儿阶段
    "l1_awareness": { name: "L1 意识世界", badge: "badge-preschool", color: "#ef4444" },
    "l2_discovery": { name: "L2 发现世界", badge: "badge-preschool", color: "#f97316" },
    "l3_invention": { name: "L3 发明世界", badge: "badge-preschool", color: "#f59e0b" },
    "l4_power": { name: "L4 动力机械", badge: "badge-preschool", color: "#eab308" },
    "l5_creation": { name: "L5 创造世界", badge: "badge-preschool", color: "#84cc16" },
    // 图形化阶段
    "spike": { name: "SPIKE", badge: "badge-kitten", color: "#10b981" },
    "kitten_k2": { name: "Kitten K2 萌新", badge: "badge-kitten", color: "#06b6d4" },
    "kitten_k4": { name: "Kitten K4 乐学", badge: "badge-kitten", color: "#3b82f6" },
    // 代码阶段
    "cpp_a1": { name: "AICODE01", badge: "badge-cpp", color: "#6366f1" },
    "cpp_a2": { name: "AICODE02", badge: "badge-cpp", color: "#8b5cf6" },
    "ai_a3": { name: "AICODE03", badge: "badge-ai", color: "#a855f7" },
    // 兼容旧路径
    "preschool": { name: "幼儿启蒙", badge: "badge-preschool", color: "#ef4444" },
    "kitten": { name: "图形化编程", badge: "badge-kitten", color: "#10b981" },
    "cpp": { name: "C++编程", badge: "badge-cpp", color: "#2563eb" },
    "ai": { name: "AI创新", badge: "badge-ai", color: "#9333ea" }
};

// ========== 全局状态 ==========
let studentDB = [];
let activeStu = null;
let editingIndex = -1;
let currentMD = "";
let surveyConfig = null;
const API_BASE = '';

// ========== 页面初始化 ==========
document.addEventListener('DOMContentLoaded', function() {
    loadApiKey();
    loadStudents();
    loadStats();
});

// ========== API Key 管理 ==========
function saveApiKey() {
    const key = document.getElementById('api_key').value.trim();
    if (key) {
        localStorage.setItem('zhipu_api_key', key);
        showToast('API Key 已保存');
    }
}

function loadApiKey() {
    const key = localStorage.getItem('zhipu_api_key') || '';
    document.getElementById('api_key').value = key;
}

// ========== 页面切换 ==========
function showPage(pageName) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(`page-${pageName}`).classList.add('active');

    if (pageName === 'student-list') {
        renderStudentGrid();
    } else if (pageName === 'archive') {
        renderLibrary();
    }

    window.scrollTo(0, 0);
}

// ========== 学生数据管理 ==========
async function loadStudents() {
    try {
        const res = await fetch(`${API_BASE}/api/students`);
        const data = await res.json();
        if (data.success) {
            studentDB = data.data;
            renderTable();
        }
    } catch (e) {
        console.error('加载学生列表失败:', e);
    }
}

async function loadStats() {
    try {
        const res = await fetch(`${API_BASE}/api/stats/overview`);
        const data = await res.json();
        if (data.success) {
            document.getElementById('stat-total').textContent = data.data.total_students;
            document.getElementById('stat-completed').textContent = data.data.surveys_completed;
            document.getElementById('stat-portraits').textContent = data.data.portraits_count;
        }
    } catch (e) {
        console.error('加载统计失败:', e);
    }
}

// ========== 学生导入/编辑 ==========
function handleMainAction() {
    if (editingIndex === -1) {
        importStudents();
    } else {
        saveEditedStudent();
    }
}

async function importStudents() {
    const raw = document.getElementById('batchInput').value.trim();
    if (!raw) return;

    try {
        const res = await fetch(`${API_BASE}/api/students/batch`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: raw })
        });
        const data = await res.json();

        if (data.success) {
            showToast(`成功导入 ${data.count} 名学生`);
            document.getElementById('batchInput').value = '';
            loadStudents();
            loadStats();
        } else {
            showToast(data.message, 'error');
        }
    } catch (e) {
        showToast('导入失败', 'error');
    }
}

function editStu(index) {
    editingIndex = index;
    const s = studentDB[index];

    document.getElementById('batchInput').style.display = 'none';
    document.getElementById('editForm').style.display = 'grid';
    document.getElementById('cancelEditBtn').style.display = 'inline-flex';

    document.getElementById('editName').value = s.name;
    document.getElementById('editSex').value = s.gender;
    document.getElementById('editClass').value = s.class_name;
    document.getElementById('editTime').value = s.class_time || '';

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function saveEditedStudent() {
    const s = studentDB[editingIndex];

    try {
        const res = await fetch(`${API_BASE}/api/students/${s.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: document.getElementById('editName').value,
                gender: document.getElementById('editSex').value,
                class_name: document.getElementById('editClass').value,
                class_time: document.getElementById('editTime').value
            })
        });
        const data = await res.json();

        if (data.success) {
            showToast('更新成功');
            cancelEdit();
            loadStudents();
        } else {
            showToast(data.message, 'error');
        }
    } catch (e) {
        showToast('更新失败', 'error');
    }
}

function cancelEdit() {
    editingIndex = -1;
    document.getElementById('batchInput').style.display = 'block';
    document.getElementById('editForm').style.display = 'none';
    document.getElementById('cancelEditBtn').style.display = 'none';
}

async function delStu(index) {
    if (!confirm('确定要删除这名学生吗？此操作不可恢复。')) return;

    const s = studentDB[index];
    try {
        const res = await fetch(`${API_BASE}/api/students/${s.id}`, { method: 'DELETE' });
        const data = await res.json();

        if (data.success) {
            showToast('删除成功');
            loadStudents();
            loadStats();
        } else {
            showToast(data.message, 'error');
        }
    } catch (e) {
        showToast('删除失败', 'error');
    }
}

// ========== 表格渲染 ==========
function renderTable() {
    const tbody = document.querySelector('#stuTable tbody');
    tbody.innerHTML = studentDB.map((s, i) => {
        const pathInfo = PATH_CONFIG[s.path] || { name: s.path, badge: 'badge-gray' };
        return `
        <tr>
            <td><b>${s.name}</b></td>
            <td>${s.class_name}</td>
            <td><span class="path-badge ${pathInfo.badge}">${pathInfo.name}</span></td>
            <td>
                ${s.has_survey
                    ? '<span class="status-dot completed"></span><span style="color:var(--success)">已完成</span>'
                    : '<span class="status-dot pending"></span><span style="color:#999">待测</span>'}
            </td>
            <td>
                <button class="btn-primary btn-small" onclick="openSurveyByIndex(${i})">填写画像</button>
                <button class="btn-warning btn-small" onclick="editStu(${i})">修正名册</button>
                <button class="btn-danger btn-small" onclick="delStu(${i})">删除</button>
            </td>
        </tr>
    `}).join('');
}

// ========== 学生网格渲染 ==========
function renderStudentGrid() {
    const grid = document.getElementById('studentGrid');
    grid.innerHTML = studentDB.map(s => {
        const pathInfo = PATH_CONFIG[s.path] || { name: s.path, badge: 'badge-gray', color: '#999' };
        return `
        <div class="stu-card" onclick="openSurveyById(${s.id})">
            <h4>${s.name}</h4>
            <small>${s.class_name}</small>
            <div style="margin-top:8px;">
                <span class="path-badge ${pathInfo.badge}">${pathInfo.name}</span>
            </div>
            <div class="status">
                ${s.has_survey
                    ? '<span class="status-completed"><i class="fas fa-check-circle"></i> 已完成</span>'
                    : '<span class="status-pending">待测评</span>'}
            </div>
        </div>
    `}).join('');
}

function openSurveyByIndex(index) {
    const s = studentDB[index];
    openSurveyById(s.id);
}

// ========== 问卷系统 ==========
async function openSurveyById(studentId) {
    const student = studentDB.find(s => s.id === studentId);
    if (!student) return;

    activeStu = student;

    // 显示学生信息
    document.getElementById('survey-student-name').textContent = student.name;
    const badge = document.getElementById('survey-path-badge');
    const pathInfo = PATH_CONFIG[student.path] || { name: student.path, badge: 'badge-gray' };
    badge.textContent = pathInfo.name;
    badge.className = `path-badge ${pathInfo.badge}`;

    // 加载问卷配置和已有进度
    await loadSurveyConfig(student.path);
    await loadSurveyProgress(studentId);

    // 渲染问卷
    renderSurvey();

    showPage('survey');
}

async function loadSurveyConfig(path) {
    try {
        const res = await fetch(`${API_BASE}/api/survey/config?path=${path}`);
        const data = await res.json();
        if (data.success) {
            surveyConfig = data.data;
        }
    } catch (e) {
        console.error('加载问卷配置失败:', e);
    }
}

let currentProgress = {};
let currentRemark = '';

async function loadSurveyProgress(studentId) {
    try {
        const res = await fetch(`${API_BASE}/api/survey/${studentId}`);
        const data = await res.json();
        if (data.success) {
            currentProgress = data.data.progress || {};
            currentRemark = data.data.remark || '';
        }
    } catch (e) {
        console.error('加载问卷进度失败:', e);
    }
}

function renderSurvey() {
    const container = document.getElementById('dynamicSurvey');
    container.innerHTML = '';

    // 通用模块
    if (surveyConfig && surveyConfig.common) {
        surveyConfig.common.forEach(group => {
            renderSurveyGroup(group, container);
        });
    }

    // 路径特定模块
    if (surveyConfig && surveyConfig.path_specific) {
        surveyConfig.path_specific.forEach(group => {
            renderSurveyGroup(group, container);
        });
    }

    updateProgress();
}

function renderSurveyGroup(group, container) {
    const section = document.createElement('div');
    section.className = 'question-section';
    section.innerHTML = `<h3>${group.group}</h3>`;

    const grid = document.createElement('div');
    grid.className = 'question-grid';

    group.items.forEach(item => {
        const savedVal = currentProgress[item.id] || (item.type === 'checkbox' ? [] : '');

        const wrap = document.createElement('div');
        wrap.className = 'q-wrap';

        const label = document.createElement('label');
        label.className = 'q-label';
        label.textContent = item.label;
        wrap.appendChild(label);

        if (item.type === 'radio' || item.type === 'checkbox') {
            const optGroup = document.createElement('div');
            optGroup.className = 'opt-group';

            item.opts.forEach(opt => {
                const isChecked = Array.isArray(savedVal)
                    ? savedVal.includes(opt)
                    : (savedVal === opt);

                const optLabel = document.createElement('label');
                optLabel.className = `opt-item ${isChecked ? 'checked' : ''}`;

                const input = document.createElement('input');
                input.type = item.type;
                input.name = item.id;
                input.value = opt;
                if (isChecked) input.checked = true;
                input.onchange = autoSave;

                optLabel.appendChild(input);
                optLabel.appendChild(document.createTextNode(opt));
                optGroup.appendChild(optLabel);
            });

            wrap.appendChild(optGroup);
        } else if (item.type === 'textarea') {
            const textarea = document.createElement('textarea');
            textarea.name = item.id;
            textarea.value = savedVal;
            textarea.placeholder = item.placeholder || '';
            textarea.rows = 4;
            textarea.oninput = autoSave;
            wrap.appendChild(textarea);
        } else {
            const input = document.createElement('input');
            input.type = 'text';
            input.name = item.id;
            input.value = savedVal;
            input.placeholder = item.placeholder || '';
            input.oninput = autoSave;
            wrap.appendChild(input);
        }

        grid.appendChild(wrap);
    });

    section.appendChild(grid);
    container.appendChild(section);
}

async function autoSave() {
    if (!activeStu) return;

    const data = {
        remark: document.getElementById('remark').value,
        progress: {}
    };

    // 收集所有输入值
    document.querySelectorAll('#dynamicSurvey input').forEach(input => {
        const name = input.name;
        if (input.type === 'checkbox') {
            if (!data.progress[name]) data.progress[name] = [];
            if (input.checked) data.progress[name].push(input.value);
        } else if (input.type === 'radio') {
            if (input.checked) data.progress[name] = input.value;
        } else {
            data.progress[name] = input.value;
        }
    });

    // 更新UI选中状态
    document.querySelectorAll('.opt-item').forEach(label => {
        const input = label.querySelector('input');
        label.classList.toggle('checked', input.checked);
    });

    currentProgress = data.progress;
    currentRemark = data.remark;

    // 发送到服务器
    try {
        await fetch(`${API_BASE}/api/survey/${activeStu.id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ progress: data.progress, remark: data.remark })
        });

        // 显示保存提示
        const hint = document.getElementById('save-hint');
        hint.innerHTML = '<i class="fas fa-check-circle"></i> 已保存';
        setTimeout(() => {
            hint.innerHTML = '<i class="fas fa-check-circle"></i> 数据已实时同步';
        }, 1000);
    } catch (e) {
        console.error('自动保存失败:', e);
    }

    updateProgress();
}

function updateProgress() {
    const total = document.querySelectorAll('.q-wrap').length;
    const done = Object.keys(currentProgress).filter(k => {
        if (k === 'remark') return false;
        const v = currentProgress[k];
        return v && (Array.isArray(v) ? v.length > 0 : v.toString().length > 0);
    }).length;

    document.getElementById('p-fill').style.width = (total ? (done / total) * 100 : 0) + '%';
    document.getElementById('p-text').innerText = `已采集数据维度: ${done}/${total}`;
}

// ========== AI 画像生成 ==========
async function generatePortrait() {
    const apiKey = document.getElementById('api_key').value.trim();
    if (!apiKey) {
        alert('请先在顶部输入 API Key');
        return;
    }

    showPage('portrait');
    document.getElementById('loading').style.display = 'block';
    document.getElementById('portraitOutput').innerHTML = '';

    try {
        const res = await fetch(`${API_BASE}/api/portrait/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: activeStu.id,
                api_key: apiKey
            })
        });

        const data = await res.json();
        document.getElementById('loading').style.display = 'none';

        if (data.success) {
            currentMD = data.data.content;
            document.getElementById('portraitOutput').innerHTML = `
                <div class="portrait-card">
                    <div class="p-header">
                        <h2>${activeStu.name}</h2>
                        <span>STATUS: ANALYZED</span>
                    </div>
                    <div class="p-body">${marked.parse(currentMD)}</div>
                </div>
            `;
            loadStats();
        } else {
            document.getElementById('portraitOutput').innerHTML = `
                <div class="error-msg">
                    <i class="fas fa-exclamation-circle"></i>
                    <p>生成失败: ${data.message}</p>
                </div>
            `;
        }
    } catch (e) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('portraitOutput').innerHTML = `
            <div class="error-msg">
                <i class="fas fa-exclamation-circle"></i>
                <p>请求失败，请检查网络连接</p>
            </div>
        `;
    }
}

async function saveToArchive() {
    showToast('画像已存入档案库');
    loadStudents();
    showPage('archive');
}

function copyPortrait() {
    if (!currentMD) return;
    navigator.clipboard.writeText(currentMD).then(() => {
        showToast('已复制 Markdown 源码');
    });
}

// ========== 档案库 ==========
async function renderLibrary() {
    const container = document.getElementById('libraryContent');
    container.innerHTML = '<div class="loading"><i class="fas fa-sync fa-spin"></i><p>加载中...</p></div>';

    try {
        const res = await fetch(`${API_BASE}/api/portrait/all`);
        const data = await res.json();

        if (data.success && data.data.length > 0) {
            container.innerHTML = data.data.map(s => {
                const pathInfo = PATH_CONFIG[s.path] || { name: s.path_name || s.path, badge: 'badge-gray' };
                return `
                <div class="stu-card" onclick="viewPortrait(${s.student_id})">
                    <h4>${s.name}</h4>
                    <small>${s.class_name}</small>
                    <div style="margin-top:10px;">
                        <span class="path-badge ${pathInfo.badge}">${pathInfo.name}</span>
                    </div>
                    <div style="margin-top:10px; font-size:12px; color:#666;">
                        ${new Date(s.created_at).toLocaleDateString()}
                    </div>
                </div>
            `}).join('');
        } else {
            container.innerHTML = '<div class="empty-state"><p>暂无档案数据</p></div>';
        }
    } catch (e) {
        container.innerHTML = '<div class="error-msg">加载失败</div>';
    }
}

async function viewPortrait(studentId) {
    try {
        const res = await fetch(`${API_BASE}/api/students/${studentId}`);
        const studentData = await res.json();

        if (studentData.success) {
            activeStu = studentData.data;
            currentMD = studentData.data.portrait_content;

            showPage('portrait');
            document.getElementById('loading').style.display = 'none';
            document.getElementById('portraitOutput').innerHTML = `
                <div class="portrait-card">
                    <div class="p-header">
                        <h2>${activeStu.name}</h2>
                        <span>HISTORICAL ARCHIVE</span>
                    </div>
                    <div class="p-body">${marked.parse(currentMD)}</div>
                </div>
            `;
        }
    } catch (e) {
        showToast('加载档案失败', 'error');
    }
}

// ========== 数据备份/恢复 ==========
async function exportBackup() {
    try {
        const res = await fetch(`${API_BASE}/api/export`);
        const data = await res.json();

        if (data.success) {
            const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `backup_${new Date().toISOString().slice(0,10)}.json`;
            a.click();
            URL.revokeObjectURL(url);
            showToast('备份文件已下载');
        }
    } catch (e) {
        showToast('备份失败', 'error');
    }
}

async function importBackup(input) {
    const file = input.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async function() {
        try {
            const jsonData = JSON.parse(reader.result);
            const res = await fetch(`${API_BASE}/api/import`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: jsonData })
            });
            const data = await res.json();

            if (data.success) {
                showToast(`成功导入 ${data.count} 条记录`);
                loadStudents();
                loadStats();
            } else {
                showToast(data.message, 'error');
            }
        } catch (e) {
            showToast('文件格式错误', 'error');
        }
    };
    reader.readAsText(file);
    input.value = '';
}

async function downloadAllMerged() {
    try {
        const res = await fetch(`${API_BASE}/api/export/portraits`);
        const data = await res.json();

        if (data.success) {
            const blob = new Blob([data.data], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `all_portraits_${new Date().toISOString().slice(0,10)}.md`;
            a.click();
            URL.revokeObjectURL(url);
            showToast('全员画像报告已下载');
        }
    } catch (e) {
        showToast('导出失败', 'error');
    }
}

// ========== 工具函数 ==========
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> ${message}`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? 'var(--success)' : 'var(--danger)'};
        color: white;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    .error-msg {
        text-align: center;
        padding: 50px;
        color: var(--danger);
    }
    .empty-state {
        text-align: center;
        padding: 50px;
        color: var(--text-light);
        grid-column: 1 / -1;
    }
    .toast {
        font-size: 14px;
        font-weight: 500;
    }
`;
document.head.appendChild(style);
