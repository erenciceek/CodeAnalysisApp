document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM yüklendi, JavaScript başlatılıyor...');
    
    // DOM elementleri
    const codeInput = document.getElementById('codeInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const clearBtn = document.getElementById('clearBtn');
    const analysisOutput = document.getElementById('analysisOutput');
    const results = document.getElementById('results');
    const fileInput = document.getElementById('fileInput');
    const fileDropZone = document.getElementById('fileDropZone');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const historyList = document.getElementById('historyList');
    const fileSelectBtn = document.getElementById('fileSelectBtn');
    const removeFileBtn = document.getElementById('removeFileBtn');
    const copyBtn = document.getElementById('copyBtn');
    const refreshBtn = document.getElementById('refreshBtn');
    const deleteAllBtn = document.getElementById('deleteAllBtn');

    // DOM elementlerinin bulunup bulunmadığını kontrol et
    console.log('DOM Elementleri:', {
        codeInput: !!codeInput,
        analyzeBtn: !!analyzeBtn,
        clearBtn: !!clearBtn,
        analysisOutput: !!analysisOutput,
        results: !!results,
        fileInput: !!fileInput,
        fileDropZone: !!fileDropZone,
        fileInfo: !!fileInfo,
        fileName: !!fileName,
        historyList: !!historyList,
        fileSelectBtn: !!fileSelectBtn,
        removeFileBtn: !!removeFileBtn,
        copyBtn: !!copyBtn,
        refreshBtn: !!refreshBtn,
        deleteAllBtn: !!deleteAllBtn
    });

    let selectedFile = null;

    // Tab sistemi
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    console.log('Tab butonları bulundu:', tabBtns.length);

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            console.log('Tab butonu tıklandı:', btn.getAttribute('data-tab'));
            const targetTab = btn.getAttribute('data-tab');
            
            // Aktif tab'ı değiştir
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(targetTab + '-tab').classList.add('active');
            
            // Dosya seçiliyse textarea'ya yükle
            if (targetTab === 'text' && selectedFile) {
                loadFileContent(selectedFile);
            }
        });
    });

    // Dosya seçimi butonu
    if (fileSelectBtn) {
        fileSelectBtn.addEventListener('click', () => {
            console.log('Dosya seçim butonu tıklandı');
            fileInput.click();
        });
        console.log('Dosya seçim butonu event listener eklendi');
    }

    // Dosya yükleme işlemleri
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
        console.log('File input event listener eklendi');
    }
    
    // Drag and drop işlemleri
    if (fileDropZone) {
        fileDropZone.addEventListener('dragover', handleDragOver);
        fileDropZone.addEventListener('dragleave', handleDragLeave);
        fileDropZone.addEventListener('drop', handleDrop);
        console.log('Drag & drop event listener\'ları eklendi');
    }

    // Dosya kaldırma butonu
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', removeFile);
        console.log('Dosya kaldırma butonu event listener eklendi');
    }

    // Kopyalama butonu
    if (copyBtn) {
        copyBtn.addEventListener('click', copyAnalysis);
        console.log('Kopyalama butonu event listener eklendi');
    }

    // Yenileme butonu
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadHistory);
        console.log('Yenileme butonu event listener eklendi');
    }

    // Tümünü sil butonu
    if (deleteAllBtn) {
        deleteAllBtn.addEventListener('click', deleteAllHistory);
        console.log('Tümünü sil butonu event listener eklendi');
    }

    // Analiz geçmişini yükle
    loadHistory();

    // Analiz butonu
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async function() {
            console.log('Analiz butonu tıklandı');
            const code = getCodeToAnalyze();
            
            if (!code) {
                showError('Lütfen analiz edilecek kodu girin veya dosya yükleyin.');
                return;
            }

            // Butonu devre dışı bırak ve loading göster
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analiz Ediliyor...';
            showLoading();

            try {
                console.log('API isteği gönderiliyor...');
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: code })
                });

                console.log('API yanıtı:', response.status);

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Analiz sırasında bir hata oluştu.');
                }

                const data = await response.json();
                showAnalysisResult(data.analysis);
                loadHistory(); // Geçmişi yenile

            } catch (error) {
                console.error('Analiz hatası:', error);
                showError('Hata: ' + error.message);
            } finally {
                // Butonu tekrar aktif et
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Kodu Analiz Et';
            }
        });
        console.log('Analiz butonu event listener eklendi');
    }

    // Temizle butonu
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            console.log('Temizle butonu tıklandı');
            codeInput.value = '';
            removeFile();
            results.style.display = 'none';
        });
        console.log('Temizle butonu event listener eklendi');
    }

    // Dosya seçimi
    function handleFileSelect(event) {
        console.log('File input change event tetiklendi');
        const file = event.target.files[0];
        if (file) {
            console.log('Dosya seçildi:', file.name, file.size);
            // Hemen dosyayı işle
            processSelectedFile(file);
            // File input'u temizle
            setTimeout(() => {
                event.target.value = '';
            }, 100);
        }
    }

    // Dosya işleme fonksiyonu
    function processSelectedFile(file) {
        console.log('Dosya işleniyor:', file.name);
        
        // Dosya doğrulaması
        const allowedExtensions = ['.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedExtensions.includes(fileExtension)) {
            showError(`Desteklenmeyen dosya türü: ${fileExtension}. Desteklenen türler: ${allowedExtensions.join(', ')}`);
            return;
        }

        if (file.size > 1024 * 1024) {
            showError('Dosya boyutu 1MB\'dan büyük olamaz.');
            return;
        }

        // UI'yi güncelle
        selectedFile = file;
        fileName.textContent = file.name;
        fileInfo.style.display = 'block';
        fileDropZone.style.display = 'none';
        
        // Dosya içeriğini hemen yükle
        loadFileContentImmediately(file);
    }

    // Drag and drop işlemleri
    function handleDragOver(e) {
        e.preventDefault();
        fileDropZone.classList.add('dragover');
    }

    function handleDragLeave(e) {
        e.preventDefault();
        fileDropZone.classList.remove('dragover');
    }

    function handleDrop(e) {
        e.preventDefault();
        fileDropZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            console.log('Drag & drop ile dosya bırakıldı:', files[0].name);
            processSelectedFile(files[0]);
        }
    }

    // Dosya içeriğini hemen yükle (yeni fonksiyon)
    function loadFileContentImmediately(file) {
        console.log('Dosya içeriği hemen okunuyor:', file.name);
        
        const reader = new FileReader();
        
        reader.onload = function(e) {
            console.log('Dosya içeriği başarıyla yüklendi:', file.name);
            codeInput.value = e.target.result;
            
            // Text tab'ına otomatik geç
            switchToTextTab();
            
            // Başarı mesajı göster
            showSuccess(`Dosya başarıyla yüklendi: ${file.name}`);
        };
        
        reader.onerror = function() {
            console.error('Dosya okuma hatası:', file.name);
            showError('Dosya okunamadı: ' + file.name);
        };
        
        reader.readAsText(file);
    }

    // Text tab'ına geç
    function switchToTextTab() {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        const textTabBtn = document.querySelector('[data-tab="text"]');
        const textTabContent = document.getElementById('text-tab');
        
        if (textTabBtn && textTabContent) {
            textTabBtn.classList.add('active');
            textTabContent.classList.add('active');
        }
    }

    // Başarı mesajı göster
    function showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `<i class="fas fa-check"></i> ${message}`;
        successDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(successDiv);
        
        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }

    // Dosya içeriğini yükle (eski fonksiyon - geriye uyumluluk için)
    function loadFileContent(file) {
        loadFileContentImmediately(file);
    }

    // Dosyayı kaldır
    function removeFile() {
        selectedFile = null;
        fileInput.value = '';
        fileInfo.style.display = 'none';
        fileDropZone.style.display = 'block';
    }

    // Analiz edilecek kodu al
    function getCodeToAnalyze() {
        return codeInput.value.trim();
    }

    // Loading göster
    function showLoading() {
        results.style.display = 'block';
        analysisOutput.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Kod analiz ediliyor, lütfen bekleyin...</div>';
    }

    // Analiz sonucunu göster (XSS korumalı)
    function showAnalysisResult(analysis) {
        results.style.display = 'block';
        // DOMPurify ile HTML'i temizle
        analysisOutput.innerHTML = DOMPurify.sanitize(analysis);
        analysisOutput.classList.add('success');
    }

    // Hata göster (XSS korumalı)
    function showError(message) {
        results.style.display = 'block';
        // DOMPurify ile HTML'i temizle
        const errorHtml = `<div class="error"><i class="fas fa-exclamation-triangle"></i> ${message}</div>`;
        analysisOutput.innerHTML = DOMPurify.sanitize(errorHtml);
        analysisOutput.classList.remove('success');
    }

    // Analiz sonucunu kopyala
    function copyAnalysis() {
        const text = analysisOutput.textContent;
        navigator.clipboard.writeText(text).then(() => {
            const copyBtn = document.querySelector('.copy-btn');
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fas fa-check"></i> Kopyalandı!';
            copyBtn.style.background = '#28a745';
            
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
                copyBtn.style.background = '#28a745';
            }, 2000);
        }).catch(err => {
            console.error('Kopyalama başarısız:', err);
        });
    }

    // Geçmişi yükle
    async function loadHistory() {
        try {
            historyList.innerHTML = '<div class="loading-history"><i class="fas fa-spinner fa-spin"></i> Geçmiş yükleniyor...</div>';
            
            const response = await fetch('/api/history');
            if (response.ok) {
                const history = await response.json();
                displayHistory(history);
            } else {
                throw new Error('Geçmiş yüklenemedi');
            }
        } catch (error) {
            console.error('Geçmiş yüklenirken hata:', error);
            historyList.innerHTML = '<div class="error">Geçmiş yüklenirken hata oluştu.</div>';
        }
    }

    // Geçmişi göster (güvenli event handling ile)
    function displayHistory(history) {
        historyList.innerHTML = '';

        if (history.length === 0) {
            historyList.innerHTML = '<div class="empty-history"><i class="fas fa-inbox"></i><p>Henüz analiz geçmişi bulunmuyor.</p></div>';
            return;
        }

        history.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            // Timestamp ve kod bilgilerini güvenli şekilde oluştur
            const timestamp = document.createElement('div');
            timestamp.className = 'history-timestamp';
            timestamp.innerHTML = '<i class="fas fa-clock"></i> ' + new Date(item.timestamp).toLocaleString('tr-TR');
            
            const codePreview = document.createElement('div');
            codePreview.className = 'history-code';
            codePreview.textContent = item.original_code.substring(0, 100) + (item.original_code.length > 100 ? '...' : '');
            
            // Görüntüle butonu - güvenli event handling
            const viewButton = document.createElement('button');
            viewButton.className = 'history-load-btn';
            viewButton.innerHTML = '<i class="fas fa-eye"></i> Görüntüle';
            
            // Sil butonu - güvenli event handling
            const deleteButton = document.createElement('button');
            deleteButton.className = 'history-delete-btn';
            deleteButton.innerHTML = '<i class="fas fa-trash"></i> Sil';
            
            // Verileri dataset'te sakla (güvenli)
            viewButton.dataset.code = item.original_code;
            viewButton.dataset.analysis = item.analysis_result;
            deleteButton.dataset.id = item.id;

            viewButton.addEventListener('click', function() {
                loadHistoryItem(this.dataset.code, this.dataset.analysis);
            });

            deleteButton.addEventListener('click', function() {
                deleteSingleHistoryItem(this.dataset.id, historyItem);
            });

            // Actions div'i
            const historyActions = document.createElement('div');
            historyActions.className = 'history-actions';
            historyActions.appendChild(viewButton);
            historyActions.appendChild(deleteButton);

            // Elementleri birleştir
            historyItem.appendChild(timestamp);
            historyItem.appendChild(codePreview);
            historyItem.appendChild(historyActions);
            
            historyList.appendChild(historyItem);
        });
    }

    // Geçmiş öğesini yükle
    function loadHistoryItem(code, analysis) {
        codeInput.value = code;
        // DOMPurify ile analiz sonucunu güvenli şekilde yükle
        analysisOutput.innerHTML = DOMPurify.sanitize(analysis);
        results.style.display = 'block';
        
        // Text tab'ına geç
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        document.querySelector('[data-tab="text"]').classList.add('active');
        document.getElementById('text-tab').classList.add('active');
    }

    // Tekli geçmiş öğesini sil
    async function deleteSingleHistoryItem(id, historyItemElement) {
        if (confirm('Bu analiz geçmişini silmek istediğinize emin misiniz?')) {
            try {
                const response = await fetch(`/api/history/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    loadHistory(); // Geçmişi yeniden yükle
                    alert('Analiz geçmişi başarıyla silindi.');
                    historyItemElement.remove(); // DOM'dan sil
                } else {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Geçmiş silinemedi.');
                }
            } catch (error) {
                console.error('Tekli silme hatası:', error);
                alert('Hata: ' + error.message);
            }
        }
    }

    // Tümünü sil butonu
    async function deleteAllHistory() {
        if (confirm('Tüm analiz geçmişini silmek istediğinize emin misiniz?')) {
            try {
                const response = await fetch('/api/history', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    loadHistory(); // Geçmişi yeniden yükle
                    alert('Tüm analiz geçmişi başarıyla silindi.');
                } else {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Geçmiş silinemedi.');
                }
            } catch (error) {
                console.error('Tümünü silme hatası:', error);
                alert('Hata: ' + error.message);
            }
        }
    }

    // Enter tuşu ile analiz başlatma
    codeInput.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            analyzeBtn.click();
        }
    });

    // Dosya yükleme alanına tıklama
    fileDropZone.addEventListener('click', function() {
        fileInput.click();
    });
});
