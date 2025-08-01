import google.generativeai as genai
import os

def analyze_code_with_gemini(code: str) -> str:
    """
    Verilen kodu Gemini API'ye gönderir ve analiz sonucunu döner.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')  # Hızlı ve uygun maliyetli model

        prompt = f"""
        Sen kıdemli bir yazılım geliştirici ve kod inceleme uzmanısın.
        Aşağıdaki kodu analiz et ve şu formatta bir rapor oluştur:

        1. **Hatalar ve Bug'lar:** Kodun çalışmasını engelleyecek veya yanlış sonuçlar üretecek potansiyel hataları listele. Eğer hata yoksa "Tespit edilmedi" yaz.
        2. **Güvenlik Açıkları:** Olası güvenlik zafiyetlerini (SQL injection, XSS, güvensiz kütüphane kullanımı vb.) belirt. Eğer açık yoksa "Tespit edilmedi" yaz.
        3. **Refactoring (Yeniden Düzenleme) Önerileri:** Kodun okunabilirliğini, performansını ve sürdürülebilirliğini artırmak için somut önerilerde bulun.
        4. **Genel Değerlendirme:** Kod hakkında kısa bir genel yorum yap.

        Analiz edilecek kod:
        ```
        {code}
        ```
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"API ile iletişimde bir hata oluştu: {str(e)}"
