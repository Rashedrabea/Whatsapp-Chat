// API Configuration
const API_BASE_URL = "http://127.0.0.1:8000";

// DOM Elements
const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const loadingState = document.getElementById("loadingState");
const resultsSection = document.getElementById("resultsSection");
const errorState = document.getElementById("errorState");
const errorMessage = document.getElementById("errorMessage");
const tabBtns = document.querySelectorAll(".tab-btn");
const tabPanes = document.querySelectorAll(".tab-pane");
const resetBtn = document.getElementById("resetBtn");
const retryBtn = document.getElementById("retryBtn");
const exportBtn = document.getElementById("exportBtn");

let currentAnalysisData = null;

// ============================================
// Event Listeners
// ============================================

uploadArea.addEventListener("click", () => fileInput.click());
uploadArea.addEventListener("dragover", handleDragOver);
uploadArea.addEventListener("dragleave", handleDragLeave);
uploadArea.addEventListener("drop", handleDrop);

fileInput.addEventListener("change", handleFileSelect);
uploadBtn.addEventListener("click", uploadFile);

tabBtns.forEach((btn) => {
  btn.addEventListener("click", () => switchTab(btn.dataset.tab));
});

resetBtn.addEventListener("click", resetAnalysis);
retryBtn.addEventListener("click", resetAnalysis);
exportBtn.addEventListener("click", exportReport);

// ============================================
// Upload Handlers
// ============================================

function handleDragOver(e) {
  e.preventDefault();
  uploadArea.style.borderColor = "#25d366";
  uploadArea.style.background = "#f1f8f5";
}

function handleDragLeave(e) {
  e.preventDefault();
  uploadArea.style.borderColor = "#25d366";
  uploadArea.style.background = "transparent";
}

function handleDrop(e) {
  e.preventDefault();
  uploadArea.style.borderColor = "#25d366";
  uploadArea.style.background = "transparent";

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    fileInput.files = files;
    uploadFile();
  }
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) {
    uploadBtn.textContent = `جاهز: ${file.name}`;
    uploadBtn.style.background = "#4caf50";
  }
}

async function uploadFile() {
  const file = fileInput.files[0];

  if (!file) {
    showError("الرجاء اختيار ملف أولاً");
    return;
  }

  if (!file.name.endsWith(".txt")) {
    showError("الرجاء اختيار ملف .txt");
    return;
  }

  try {
    showLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/upload/`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.status === "success") {
      currentAnalysisData = data.data;
      showResults(data.data);
    } else {
      showError(data.error || "خطأ في معالجة الملف");
    }
  } catch (error) {
    console.error("Error:", error);
    showError(
      "خطأ في الاتصال بالخادم. تأكد من تشغيل الخادم على: " + API_BASE_URL,
    );
  } finally {
    showLoading(false);
  }
}

// ============================================
// Results Display
// ============================================

function showResults(data) {
  // Hide other states
  errorState.style.display = "none";
  uploadArea.parentElement.parentElement.style.display = "none";

  // Show results
  resultsSection.style.display = "block";

  // Update stats
  updateStats(data);

  // Populate tabs
  populateWordsTab(data);
  populateEmojisTab(data);
  populateUsersTab(data);
  populateSentimentTab(data);
}

function updateStats(data) {
  const totalMessages = Object.values(
    data.total_messages_per_user || {},
  ).reduce((a, b) => a + b, 0);
  const totalUsers = Object.keys(data.total_messages_per_user || {}).length;
  const totalEmojis = data.top_emojis_used ? data.top_emojis_used.length : 0;
  const totalLinks = data.most_common_links ? data.most_common_links.length : 0;

  document.getElementById("totalMessages").textContent = totalMessages;
  document.getElementById("totalUsers").textContent = totalUsers;
  document.getElementById("totalEmojis").textContent = totalEmojis;
  document.getElementById("totalLinks").textContent = totalLinks;
}

function populateWordsTab(data) {
  const wordsList = document.getElementById("wordsList");
  wordsList.innerHTML = "";

  if (data.top_words && data.top_words.length > 0) {
    data.top_words.forEach(([word, count]) => {
      const li = document.createElement("li");
      li.innerHTML = `
                <span class="word">${word}</span>
                <span class="count">${count}</span>
            `;
      wordsList.appendChild(li);
    });
  } else {
    wordsList.innerHTML = '<li style="text-align: center;">لا توجد بيانات</li>';
  }
}

function populateEmojisTab(data) {
  const emojisGrid = document.getElementById("emojisGrid");
  emojisGrid.innerHTML = "";

  if (data.top_emojis_used && data.top_emojis_used.length > 0) {
    data.top_emojis_used.forEach(([emoji, count]) => {
      const div = document.createElement("div");
      div.className = "emoji-item";
      div.innerHTML = `
                <div class="emoji-char">${emoji}</div>
                <div class="emoji-count">${count}</div>
            `;
      emojisGrid.appendChild(div);
    });
  } else {
    emojisGrid.innerHTML = "<p>لا توجد بيانات</p>";
  }
}

function populateUsersTab(data) {
  const usersGrid = document.getElementById("usersGrid");
  usersGrid.innerHTML = "";

  if (data.total_messages_per_user) {
    Object.entries(data.total_messages_per_user).forEach(([user, msgCount]) => {
      const avgResponse = data.average_response_time[user] || 0;
      const sentiment = data.sentiment_analysis[user] || 5;
      const energy = data.chat_energy_score[user] || 0;

      const div = document.createElement("div");
      div.className = "user-card";
      div.innerHTML = `
                <div class="user-name">👤 ${user}</div>
                <div class="user-stat">
                    <span class="user-stat-label">💬 الرسائل:</span>
                    <span class="user-stat-value">${msgCount}</span>
                </div>
                <div class="user-stat">
                    <span class="user-stat-label">⏳ الاستجابة:</span>
                    <span class="user-stat-value">${avgResponse.toFixed(1)} دقيقة</span>
                </div>
                <div class="user-stat">
                    <span class="user-stat-label">❤️ المشاعر:</span>
                    <span class="user-stat-value">${sentiment.toFixed(1)}/10</span>
                </div>
                <div class="user-stat">
                    <span class="user-stat-label">⚡ الطاقة:</span>
                    <span class="user-stat-value">${energy.toFixed(1)}/10</span>
                </div>
            `;
      usersGrid.appendChild(div);
    });
  } else {
    usersGrid.innerHTML = "<p>لا توجد بيانات</p>";
  }
}

function populateSentimentTab(data) {
  const sentimentGrid = document.getElementById("sentimentGrid");
  sentimentGrid.innerHTML = "";

  if (data.sentiment_analysis) {
    Object.entries(data.sentiment_analysis).forEach(([user, sentiment]) => {
      const energy = data.chat_energy_score[user] || 0;
      const sentimentPercent = Math.min(100, (sentiment / 10) * 100);
      const energyPercent = Math.min(100, (energy / 10) * 100);

      const div = document.createElement("div");
      div.className = "sentiment-card";
      div.innerHTML = `
                <div class="sentiment-header">${user}</div>
                <div>
                    <div style="margin-bottom: 15px;">
                        <div style="font-size: 12px; margin-bottom: 5px;">المشاعر: ${sentiment.toFixed(1)}/10</div>
                        <div class="sentiment-meter">
                            <div class="sentiment-bar" style="width: ${sentimentPercent}%"></div>
                        </div>
                    </div>
                    <div>
                        <div style="font-size: 12px; margin-bottom: 5px;">الطاقة: ${energy.toFixed(1)}/10</div>
                        <div class="sentiment-meter">
                            <div class="sentiment-bar" style="width: ${energyPercent}%"></div>
                        </div>
                    </div>
                </div>
            `;
      sentimentGrid.appendChild(div);
    });
  } else {
    sentimentGrid.innerHTML = "<p>لا توجد بيانات</p>";
  }
}

// ============================================
// Tab Navigation
// ============================================

function switchTab(tabName) {
  // Hide all tabs
  tabPanes.forEach((pane) => pane.classList.remove("active"));

  // Deactivate all buttons
  tabBtns.forEach((btn) => btn.classList.remove("active"));

  // Show selected tab
  document.getElementById(`${tabName}-tab`).classList.add("active");

  // Activate button
  event.target.closest(".tab-btn").classList.add("active");
}

// ============================================
// UI State Management
// ============================================

function showLoading(show) {
  loadingState.style.display = show ? "flex" : "none";
}

function showError(message) {
  errorState.style.display = "block";
  resultsSection.style.display = "none";
  uploadArea.parentElement.parentElement.style.display = "block";
  errorMessage.textContent = message;
}

function resetAnalysis() {
  fileInput.value = "";
  uploadBtn.textContent = "رفع الملف";
  uploadBtn.style.background = "";
  resultsSection.style.display = "none";
  errorState.style.display = "none";
  uploadArea.parentElement.parentElement.style.display = "block";
  currentAnalysisData = null;
}

// ============================================
// Export Report
// ============================================

function exportReport() {
  if (!currentAnalysisData) return;

  const reportContent = generateReportHTML(currentAnalysisData);
  const blob = new Blob([reportContent], { type: "text/html;charset=utf-8;" });
  const link = document.createElement("a");
  const url = URL.createObjectURL(blob);

  link.setAttribute("href", url);
  link.setAttribute(
    "download",
    `تقرير_التحليل_${new Date().toISOString().split("T")[0]}.html`,
  );
  link.style.visibility = "hidden";

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function generateReportHTML(data) {
  const totalMessages = Object.values(
    data.total_messages_per_user || {},
  ).reduce((a, b) => a + b, 0);

  return `
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>تقرير تحليل المحادثة</title>
    <style>
        body { font-family: Arial, sans-serif; direction: rtl; padding: 20px; background: #f5f5f5; }
        .header { background: #075e54; color: white; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
        .header h1 { margin: 0; }
        .section { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .section h2 { color: #075e54; border-bottom: 2px solid #25d366; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 12px; text-align: right; border-bottom: 1px solid #ddd; }
        th { background: #f5f5f5; font-weight: bold; color: #075e54; }
        .stat { display: inline-block; background: #25d366; color: white; padding: 10px 20px; margin: 5px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 تقرير تحليل محادثات واتساب</h1>
        <p>تم إنشاء التقرير في: ${new Date().toLocaleDateString("ar-EG")}</p>
    </div>

    <div class="section">
        <h2>📈 الإحصائيات العامة</h2>
        <div>
            <span class="stat">إجمالي الرسائل: ${totalMessages}</span>
            <span class="stat">عدد المستخدمين: ${Object.keys(data.total_messages_per_user || {}).length}</span>
            <span class="stat">الرموز التعبيرية: ${(data.top_emojis_used || []).length}</span>
            <span class="stat">الروابط المشاركة: ${(data.most_common_links || []).length}</span>
        </div>
    </div>

    <div class="section">
        <h2>📝 أكثر الكلمات استخداماً</h2>
        <table>
            <tr><th>الكلمة</th><th>عدد الاستخدامات</th></tr>
            ${(data.top_words || [])
              .map(
                ([word, count]) => `<tr><td>${word}</td><td>${count}</td></tr>`,
              )
              .join("")}
        </table>
    </div>

    <div class="section">
        <h2>👥 إحصائيات المستخدمين</h2>
        <table>
            <tr>
                <th>المستخدم</th>
                <th>عدد الرسائل</th>
                <th>درجة المشاعر</th>
                <th>درجة الطاقة</th>
            </tr>
            ${Object.entries(data.total_messages_per_user || {})
              .map(
                ([user, count]) => `
                <tr>
                    <td>${user}</td>
                    <td>${count}</td>
                    <td>${(data.sentiment_analysis[user] || 5).toFixed(1)}/10</td>
                    <td>${(data.chat_energy_score[user] || 0).toFixed(1)}/10</td>
                </tr>
            `,
              )
              .join("")}
        </table>
    </div>
</body>
</html>
    `;
}

// ============================================
// Initialize
// ============================================

console.log("✅ تم تحميل جميع البيانات بنجاح");
console.log("🔌 الخادم على:", API_BASE_URL);
