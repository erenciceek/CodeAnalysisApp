import pytest
import json
import os
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# .env dosyasını yükle
load_dotenv()
os.environ["DATABASE_PATH"] = "test_db.sqlite3"
from app.main import app
from app.gemini_client import analyze_code_with_gemini
from app.database import init_db, save_analysis, get_history

client = TestClient(app)

class TestCodeAnalysis:
    """Kod analizi testleri"""
    
    def test_empty_code_analysis(self):
        """Boş kod gönderildiğinde hata döner"""
        response = client.post("/api/analyze", json={"code": ""})
        assert response.status_code == 400
        assert "boş olamaz" in response.json()["detail"]
    
    def test_whitespace_only_code(self):
        """Sadece boşluk içeren kod için hata döner"""
        response = client.post("/api/analyze", json={"code": "   \n\t  "})
        assert response.status_code == 400
    
    def test_valid_code_analysis(self):
        """Geçerli kod analizi testi"""
        test_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
        """
        response = client.post("/api/analyze", json={"code": test_code})
        assert response.status_code == 200
        assert "analysis" in response.json()
    
    @patch('app.main.analyze_code_with_gemini')
    def test_code_with_security_issues(self, mock_analyze):
        """Güvenlik açığı içeren kod testi"""
        # Mock analiz sonucu
        mock_analyze.return_value = """
        1. Hatalar ve Bug'lar: Tespit edilmedi
        2. Güvenlik Açıkları: Bu kod güvenlik açığı içeriyor. subprocess.run ile shell=True kullanımı command injection'a açık.
        3. Refactoring Önerileri: Güvenli alternatifler kullanılmalı
        4. Genel Değerlendirme: Güvenlik açığı var
        """
        
        test_code = """
import subprocess
user_input = input("Enter command: ")
subprocess.run(user_input, shell=True)
        """
        response = client.post("/api/analyze", json={"code": test_code})
        assert response.status_code == 200
        result = response.json()["analysis"]
        assert "güvenlik" in result.lower() or "security" in result.lower()

class TestDatabaseOperations:
    """Veritabanı işlemleri testleri"""
    
    def test_save_and_retrieve_analysis(self):
        """Analiz kaydetme ve alma testi"""
        test_code = "print('Hello World')"
        test_result = "Test analysis result"
        
        save_analysis(test_code, test_result)
        history = get_history()
        
        assert len(history) > 0
        assert history[0][2] == test_code  # original_code
        assert history[0][3] == test_result  # analysis_result
    
    def test_database_initialization(self):
        """Veritabanı başlatma testi"""
        # Bu test veritabanının başarıyla oluşturulduğunu kontrol eder
        init_db()
        # Eğer hata olursa exception fırlatır, bu yüzden buraya kadar gelirse başarılı

class TestAPIEndpoints:
    """API endpoint testleri"""
    
    def test_root_endpoint(self):
        """Ana sayfa endpoint testi"""
        response = client.get("/")
        assert response.status_code == 200
        assert "html" in response.headers["content-type"]
    
    def test_health_check(self):
        """Sağlık kontrolü endpoint testi"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Kod Gözcüsü"
    
    def test_history_endpoint(self):
        """Geçmiş endpoint testi"""
        response = client.get("/api/history")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_invalid_json_payload(self):
        """Geçersiz JSON payload testi"""
        response = client.post("/api/analyze", data="invalid json")
        assert response.status_code == 422

class TestGeminiIntegration:
    """Gemini API entegrasyon testi - analyze_code_with_gemini main üzerinden çağrıldığında"""

    @patch.dict(os.environ, {}, clear=True)
    def test_gemini_error_handling(self):
        """API key eksikse backend'den uygun hata alınmalı"""
        response = client.post("/api/analyze", json={"code": "print('test')"})
        assert response.status_code == 200
        assert "api anahtarı" in response.json()["analysis"].lower()

    @patch('app.main.analyze_code_with_gemini')
    def test_gemini_analysis_function(self, mock_analyze):
        """Mock edilmiş analiz fonksiyonu başarılı dönüş yapmalı"""
        mock_analyze.return_value = "Mock analiz sonucu"
        response = client.post("/api/analyze", json={"code": "print('test')"})
        assert response.status_code == 200
        assert response.json()["analysis"] == "Mock analiz sonucu"

class TestCodeQualityAnalysis:
    """Kod kalitesi analizi testleri"""
    
    @patch('app.main.analyze_code_with_gemini')
    def test_refactoring_suggestions(self, mock_analyze):
        """Refactoring önerileri testi"""
        mock_analyze.return_value = """
        1. Hatalar ve Bug'lar: Tespit edilmedi
        2. Güvenlik Açıkları: Tespit edilmedi
        3. Refactoring Önerileri: Bu kod daha verimli hale getirilebilir. List comprehension kullanarak daha Pythonic yazılabilir: [i for i in range(10)]
        4. Genel Değerlendirme: Kod çalışıyor ama optimize edilebilir
        """
        
        test_code = """
def bad_function():
    x = []
    for i in range(10):
        x.append(i)
    return x
        """
        response = client.post("/api/analyze", json={"code": test_code})
        assert response.status_code == 200
        result = response.json()["analysis"]
        # Refactoring önerileri içermeli
        assert len(result) > 100  # Detaylı analiz olmalı
    
    @patch('app.main.analyze_code_with_gemini')
    def test_bug_detection(self, mock_analyze):
        """Hata tespiti testi"""
        mock_analyze.return_value = """
        1. Hatalar ve Bug'lar: ZeroDivisionError oluşabilir. y=0 olduğunda x/y işlemi hata verir.
        2. Güvenlik Açıkları: Tespit edilmedi
        3. Refactoring Önerileri: Sıfıra bölme kontrolü eklenmelidir
        4. Genel Değerlendirme: Potansiyel hata var
        """
        
        test_code = """
def buggy_function():
    x = 10
    y = 0
    return x / y  # ZeroDivisionError
        """
        response = client.post("/api/analyze", json={"code": test_code})
        assert response.status_code == 200
        result = response.json()["analysis"]
        # Hata tespiti yapılmalı
        assert len(result) > 50

class TestPerformanceAndSecurity:
    """Performans ve güvenlik testleri"""
    
    @patch('app.main.analyze_code_with_gemini')
    def test_large_code_handling(self, mock_analyze):
        """Büyük kod parçası işleme testi"""
        mock_analyze.return_value = "Büyük kod analizi tamamlandı"
        large_code = "print('Hello')\n" * 1000
        response = client.post("/api/analyze", json={"code": large_code})
        assert response.status_code == 200
    
    @patch('app.main.analyze_code_with_gemini')
    def test_sql_injection_detection(self, mock_analyze):
        """SQL injection tespiti testi"""
        mock_analyze.return_value = """
        1. Hatalar ve Bug'lar: Tespit edilmedi
        2. Güvenlik Açıkları: SQL Injection riski var. Kullanıcı girdisi doğrudan SQL sorgusuna ekleniyor.
        3. Refactoring Önerileri: Parametrized queries kullanılmalı
        4. Genel Değerlendirme: Güvenlik açığı var
        """
        
        test_code = """
import sqlite3
user_input = input("Enter name: ")
query = f"SELECT * FROM users WHERE name = '{user_input}'"
        """
        response = client.post("/api/analyze", json={"code": test_code})
        assert response.status_code == 200
        result = response.json()["analysis"]
        # Güvenlik uyarısı içermeli
        assert len(result) > 50

# ============================================================================
# UNIT TESTLER - Sadece tek fonksiyon/modül test eder
# ============================================================================
class TestUnitGeminiClient:
    """Gemini client unit testleri - Sadece analyze_code_with_gemini fonksiyonunu test eder"""

    @patch.dict(os.environ, {}, clear=True)
    def test_analyze_code_with_gemini_no_api_key(self):
        """API anahtarı olmadığında uygun mesaj dönmeli"""
        result = analyze_code_with_gemini("print('test')")
        assert isinstance(result, str)
        assert "api anahtarı" in result.lower()

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake-key"})
    @patch('google.generativeai.GenerativeModel')
    def test_analyze_code_with_gemini_with_api_key(self, mock_model):
        """Geçerli API anahtarıyla düzgün analiz yapılmalı"""
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value.text = "Test analiz sonucu"
        mock_model.return_value = mock_instance

        result = analyze_code_with_gemini("print('test')")
        assert isinstance(result, str)
        assert result == "Test analiz sonucu"

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake-key"})
    @patch('google.generativeai.GenerativeModel')
    def test_analyze_code_with_gemini_exception_handling(self, mock_model):
        """API çağrısı hata verirse düzgün mesaj dönmeli"""
        mock_instance = MagicMock()
        mock_instance.generate_content.side_effect = Exception("Simulated Gemini failure")
        mock_model.return_value = mock_instance

        result = analyze_code_with_gemini("print('test')")
        assert isinstance(result, str)
        assert "hata" in result.lower()



class TestUnitDatabase:
    """Database unit testleri - Sadece database fonksiyonlarını test eder"""
    
    def test_save_analysis_unit(self):
        """Sadece save_analysis fonksiyonunu test eder"""
        test_code = "print('unit test')"
        test_result = "Unit test result"
        
        # Fonksiyonu direkt çağır
        save_analysis(test_code, test_result)
        
        # Sonucu kontrol et
        history = get_history()
        assert len(history) > 0
        
        # En son eklenen kaydı bul
        latest_record = history[0]  # En son eklenen
        assert latest_record[2] == test_code  # original_code
        assert latest_record[3] == test_result  # analysis_result
    
    def test_get_history_unit(self):
        """Sadece get_history fonksiyonunu test eder"""
        # Önce test verisi ekle
        test_code = "print('history test')"
        test_result = "History test result"
        save_analysis(test_code, test_result)
        
        # get_history fonksiyonunu test et
        history = get_history()
        
        # Sonuçları kontrol et
        assert isinstance(history, list)
        assert len(history) > 0
        
        # Her kayıt tuple olmalı
        for record in history:
            assert isinstance(record, tuple)
            assert len(record) == 4  # id, timestamp, original_code, analysis_result
    
    def test_init_db_unit(self):
        """Sadece init_db fonksiyonunu test eder"""
        # init_db fonksiyonu exception fırlatmamalı
        try:
            init_db()
            # Eğer buraya kadar gelirse başarılı
            assert True
        except Exception as e:
            assert False, f"init_db fonksiyonu hata fırlattı: {e}"

class TestUnitMainFunctions:
    """Main modülündeki fonksiyonların unit testleri"""
    
    def test_health_check_function(self):
        """Health check fonksiyonunu test eder - HTTP endpoint olarak test eder"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["status"] == "healthy"
        assert data["service"] == "Kod Gözcüsü"
    
    def test_get_analysis_history_function(self):
        """get_analysis_history fonksiyonunu test eder - HTTP endpoint olarak test eder"""
        # Test verisi ekle
        test_code = "print('main test')"
        test_result = "Main test result"
        save_analysis(test_code, test_result)
        
        # HTTP endpoint olarak test et
        response = client.get("/api/history")
        assert response.status_code == 200
        result = response.json()
        
        # Sonucu kontrol et
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Her kayıt dict olmalı
        for record in result:
            assert isinstance(record, dict)
            assert "id" in record
            assert "timestamp" in record
            assert "original_code" in record
            assert "analysis_result" in record

if __name__ == "__main__":
    pytest.main([__file__])