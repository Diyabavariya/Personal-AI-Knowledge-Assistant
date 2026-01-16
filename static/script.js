/**
 * Personal AI Assistant - Frontend Script
 * Flask-compatible (NO AJAX chat)
 */

(function () {
    'use strict';

    // DOM Elements
    const elements = {
        uploadArea: document.getElementById('uploadArea'),
        fileInput: document.getElementById('fileInput'),
        fileList: document.getElementById('fileList'),
        uploadBtn: document.getElementById('uploadBtn'),
        chatForm: document.getElementById('chatForm'),
        questionInput: document.getElementById('questionInput'),
        resetBtn: document.getElementById('resetBtn'),
        loadingOverlay: document.getElementById('loadingOverlay')
    };

    let selectedFiles = [];

    function init() {
        setupEventListeners();
        setupTextareaAutoResize();
    }

    function setupEventListeners() {
        // Upload UI
        elements.uploadArea.addEventListener('click', () => elements.fileInput.click());
        elements.fileInput.addEventListener('change', handleFileSelect);
        elements.uploadArea.addEventListener('dragover', e => e.preventDefault());
        elements.uploadArea.addEventListener('drop', handleDrop);
        elements.uploadBtn.addEventListener('click', handleUpload);

        // Reset
        elements.resetBtn.addEventListener('click', handleReset);

        // IMPORTANT: NO JS CHAT HANDLER
        // Chat is handled by normal HTML form submit
    }

    function setupTextareaAutoResize() {
        const textarea = elements.questionInput;
        textarea.addEventListener('input', () => {
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
        });
    }

    /* ---------------- FILE HANDLING ---------------- */

    function handleFileSelect(e) {
        addFiles(Array.from(e.target.files));
    }

    function handleDrop(e) {
        e.preventDefault();
        addFiles(Array.from(e.dataTransfer.files));
    }

    function addFiles(files) {
        files.forEach(file => {
            if (!selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
                selectedFiles.push(file);
            }
        });
        renderFileList();
        elements.uploadBtn.disabled = selectedFiles.length === 0;
    }

    function renderFileList() {
        elements.fileList.innerHTML = selectedFiles.map(
            (file, i) => `
            <div class="file-item">
                <span>${file.name}</span>
                <button type="button" data-i="${i}">✕</button>
            </div>`
        ).join('');

        elements.fileList.querySelectorAll('button').forEach(btn => {
            btn.onclick = () => {
                selectedFiles.splice(btn.dataset.i, 1);
                renderFileList();
                elements.uploadBtn.disabled = selectedFiles.length === 0;
            };
        });
    }

    function handleUpload() {
        if (selectedFiles.length === 0) return;

        showLoading();

        const formData = new FormData();
        selectedFiles.forEach(file => formData.append('files', file));

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(() => location.reload())
        .catch(() => alert("Upload failed"))
        .finally(hideLoading);
    }

    /* ---------------- RESET ---------------- */

    function handleReset() {
        if (!confirm("Reset session?")) return;

        showLoading();
        fetch('/reset', { method: 'POST' })
            .then(() => location.reload())
            .finally(hideLoading);
    }

    /* ---------------- UI ---------------- */

    function showLoading() {
        elements.loadingOverlay.classList.add('active');
    }

    function hideLoading() {
        elements.loadingOverlay.classList.remove('active');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
