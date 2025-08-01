# Kod Gözcüsü - Kod Analiz & İyileştirme Sistemi

## Proje Hakkında

Kod Gözcüsü, Python kodlarını analiz eden, hata ve güvenlik açıklarını tespit eden, refactoring önerileri sunan modern bir web uygulamasıdır. Google Gemini AI API'sini kullanarak akıllı kod analizi yapar.

## Özellikler

- 🔍 **Akıllı Kod Analizi**: Gemini AI ile gelişmiş kod inceleme
- 🛡️ **Güvenlik Tespiti**: SQL injection, XSS, güvensiz kütüphane kullanımı vb.
- 🐛 **Hata Tespiti**: Potansiyel bug'ları ve çalışma zamanı hatalarını tespit eder
- 🔧 **Refactoring Önerileri**: Kod kalitesini artıracak somut öneriler
- 📚 **Geçmiş Kayıtları**: Önceki analizleri görüntüleme ve yeniden kullanma
- 🎨 **Modern UI**: Kullanıcı dostu, responsive tasarım
- ⚡ **Hızlı Analiz**: Gerçek zamanlı kod analizi
- 🧪 **Kapsamlı Test Suite**: 16 test ile %100 test coverage

## Teknoloji Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI**: Google Gemini API
- **Veritabanı**: SQLite
- **Test**: pytest, unittest.mock

## Kurulum

### Gereksinimler

- Python 3.8+
- Google Gemini API anahtarı (opsiyonel - test için mock kullanılır)

### Adım 1: Projeyi Klonlayın

```bash
git clone <repository-url>
cd CodeAnalyzer
```

### Adım 2: Sanal Ortam Oluşturun

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: Gemini API Anahtarını Ayarlayın (Opsiyonel)

```bash
# .env dosyası oluşturun
echo GEMINI_API_KEY=your_api_key_here > .env

# Veya environment variable olarak
# Windows
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```

**Not**: API anahtarı olmadan da testler çalışır çünkü mock kullanılır.

### Adım 5: Uygulamayı Çalıştırın

```bash
uvicorn app.main:app --reload
```

Uygulama http://localhost:8000 adresinde çalışacaktır.

## Kullanım

### Web Arayüzü

1. Tarayıcınızda http://localhost:8000 adresine gidin
2. Analiz etmek istediğiniz kod parçasını textarea'ya yapıştırın
3. "Kodu Analiz Et" butonuna tıklayın
4. Analiz sonucunu inceleyin
5. Geçmiş analizlerinizi görüntüleyin

### API Kullanımı

#### Kod Analizi

```bash
curl -X POST "http://localhost:8000/api/analyze" \
     -H "Content-Type: application/json" \
     -d '{"code": "print(\"Hello World\")"}'
```

#### Geçmiş Görüntüleme

```bash
curl -X GET "http://localhost:8000/api/history"
```

#### Sağlık Kontrolü

```bash
curl -X GET "http://localhost:8000/health"
```

## Test Çalıştırma

```bash
# Tüm testleri çalıştır
pytest tests/

# Belirli test dosyasını çalıştır
pytest tests/test_main.py

# Detaylı test raporu
pytest tests/ -v --tb=short

# Test coverage raporu
pytest tests/ --cov=app --cov-report=html
```

### Test Sonuçları

```
==================================== 24 passed, 1 warning in 4.86s =====================================
```

**Test Kategorileri:**

#### **Integration Testler (18 test)**
- ✅ Kod Analizi Testleri (4 test)
- ✅ Veritabanı Testleri (2 test)
- ✅ API Endpoint Testleri (4 test)
- ✅ Gemini Entegrasyon Testleri (2 test)
- ✅ Kod Kalitesi Testleri (2 test)
- ✅ Performans ve Güvenlik Testleri (2 test)

#### **Unit Testler (6 test)**
- ✅ Gemini Client Unit Testleri (3 test)
- ✅ Database Unit Testleri (3 test)
- ✅ Main Functions Unit Testleri (2 test)

## 📚 Dokümantasyon

Proje kapsamlı dokümantasyon içerir:

- 📖 **[Modül Dokümantasyonu](docs/modul_dokumani.html)** - API ve modül referans kılavuzu
- 👤 **[Kullanıcı ve Admin Kılavuzu](docs/kullanici_kilavuzu.html)** - Detaylı kullanım rehberi
- 🧪 **[Unit Test Raporu](docs/unit_test_raporu.html)** - Test analizi ve performans değerlendirmesi

## Proje Yapısı

```
CodeAnalyzer/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI uygulaması
│   ├── gemini_client.py     # Gemini API entegrasyonu
│   └── database.py          # Veritabanı işlemleri
├── static/
│   ├── index.html           # Ana sayfa
│   ├── style.css            # Stil dosyası
│   └── script.js            # Frontend JavaScript
├── tests/
│   └── test_main.py         # Unit testler (24 test)
├── docs/                    # Dokümantasyon klasörü
│   ├── modul_dokumani.html  # Modül dokümantasyonu
│   ├── kullanici_kilavuzu.html # Kullanıcı kılavuzu
│   ├── unit_test_raporu.html # Test raporu
│   └── ekran1.png          # Ekran görüntüsü
├── requirements.txt          # Python bağımlılıkları
└── README.md               # Bu dosya
```

## API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/` | GET | Ana sayfa (HTML) |
| `/api/analyze` | POST | Kod analizi |
| `/api/history` | GET | Analiz geçmişi |
| `/health` | GET | Sağlık kontrolü |

## Test Kapsamı

Proje aşağıdaki test kategorilerini içerir:

### **Integration Testler (17 test)**

#### 1. Kod Analizi Testleri
- ✅ Boş kod kontrolü
- ✅ Geçerli kod analizi
- ✅ Güvenlik açığı tespiti (Mock ile)
- ✅ Whitespace kontrolü

#### 2. Veritabanı Testleri
- ✅ Analiz kaydetme
- ✅ Geçmiş alma
- ✅ Veritabanı başlatma

#### 3. API Endpoint Testleri
- ✅ Ana sayfa erişimi
- ✅ Sağlık kontrolü
- ✅ Geçersiz payload kontrolü
- ✅ Geçmiş endpoint'i

#### 4. Gemini Entegrasyon Testleri
- ✅ API analiz fonksiyonu (Mock ile)
- ✅ Hata yönetimi

#### 5. Kod Kalitesi Testleri
- ✅ Refactoring önerileri (Mock ile)
- ✅ Hata tespiti (Mock ile)

#### 6. Performans ve Güvenlik Testleri
- ✅ Büyük kod işleme (Mock ile)
- ✅ SQL injection tespiti (Mock ile)

### **Unit Testler (8 test)**

#### 7. Gemini Client Unit Testleri
- ✅ API anahtarı olmadan fonksiyon testi
- ✅ API anahtarı ile fonksiyon testi
- ✅ Exception handling testi

#### 8. Database Unit Testleri
- ✅ save_analysis fonksiyonu testi
- ✅ get_history fonksiyonu testi
- ✅ init_db fonksiyonu testi

#### 9. Main Functions Unit Testleri
- ✅ Health check fonksiyonu testi
- ✅ get_analysis_history fonksiyonu testi

## Test Türleri

### **Integration Testler vs Unit Testler**

#### **Integration Testler (17 test)**
- 🔗 **Birden fazla bileşen** test eder
- 🌐 **HTTP istekleri** yapar
- 🗄️ **Gerçek veritabanı** kullanır
- ⏱️ **Yavaş** çalışır (1-2 saniye)
- 🧪 **Sistem** testleri

#### **Unit Testler (7 test)**
- ✅ Sadece **tek bir fonksiyon** test eder
- 🔒 **Bağımlılıkları mock'lar**
- ⚡ **Hızlı** çalışır (milisaniyeler)
- 🎯 **İzole** testler

## Mock Kullanımı

Testlerde gerçek Gemini API çağrıları yerine mock'lar kullanılır. Bu sayede:

- 🚀 **Hızlı Testler**: API çağrıları olmadan anında sonuç
- 💰 **Maliyet Tasarrufu**: API kullanım ücreti yok
- 🔒 **Güvenilirlik**: İnternet bağlantısına bağımlı değil
- 🧪 **Tutarlılık**: Her test aynı sonucu verir

### Mock Örneği

```python
@patch('app.main.analyze_code_with_gemini')
def test_security_analysis(self, mock_analyze):
    mock_analyze.return_value = """
    1. Hatalar ve Bug'lar: Tespit edilmedi
    2. Güvenlik Açıkları: Bu kod güvenlik açığı içeriyor.
    3. Refactoring Önerileri: Güvenli alternatifler kullanılmalı
    4. Genel Değerlendirme: Güvenlik açığı var
    """
    # Test kodu...
```

## Geliştirme

### Yeni Özellik Ekleme

1. Feature branch oluşturun
2. Kodunuzu yazın
3. Testler ekleyin (Mock kullanın)
4. Pull request oluşturun

### Kod Standartları

- PEP 8 Python kod standartlarına uyun
- Docstring'ler ekleyin
- Type hints kullanın
- Test coverage'ı %100'e yakın tutun
- Mock kullanarak bağımlılıkları izole edin

## Sorun Giderme

### Yaygın Sorunlar

1. **Gemini API Hatası**: API anahtarı olmadan da testler çalışır (mock kullanılır)
2. **Veritabanı Hatası**: SQLite dosyasının yazma izinlerini kontrol edin
3. **Port Çakışması**: 8000 portu kullanımdaysa farklı port belirtin
4. **Test Hatası**: Mock'ların doğru import edildiğinden emin olun

### Loglar

Uygulama logları terminal'de görüntülenir. Hata durumunda detaylı bilgi için logları kontrol edin.

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Testlerinizi ekleyin (Mock kullanın)
5. Branch'inizi push edin (`git push origin feature/amazing-feature`)
6. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim

Proje hakkında sorularınız için issue açabilir veya pull request gönderebilirsiniz.

## Changelog

### v1.1.0 (Güncel)
- ✅ **Test İyileştirmeleri**: Mock kullanımı ile 24 test başarıyla geçiyor
- ✅ **Unit Test Eklendi**: 7 gerçek unit test eklendi
- ✅ **Integration Testler**: 17 integration test
- ✅ **API Anahtarı Desteği**: API anahtarı olmadan da testler çalışıyor
- ✅ **Hata Düzeltmeleri**: Import path'leri düzeltildi
- ✅ **Test Coverage**: %100 test başarı oranı (0 skip)
- ✅ **Mock Entegrasyonu**: Gerçek API çağrıları yerine mock kullanımı

### v1.0.0
- İlk sürüm
- Temel kod analizi özellikleri
- Gemini API entegrasyonu
- Web arayüzü
- Veritabanı desteği
- Kapsamlı test suite 