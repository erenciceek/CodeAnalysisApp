from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from .gemini_client import analyze_code_with_gemini
from .database import init_db, save_analysis, get_history, delete_analysis, delete_all_analyses

# .env dosyasını proje kök dizininden yükle
from pathlib import Path
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'


load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Kod Gözcüsü", description="Kod Analiz & İyileştirme Sistemi")

# Veritabanını başlat
init_db()

# Static dosyaları serve et
app.mount("/static", StaticFiles(directory="static"), name="static")

class CodeInput(BaseModel):
    code: str

@app.get("/")
async def read_root():
    """Ana sayfa - index.html dosyasını döner"""
    return FileResponse("static/index.html")

@app.post("/api/analyze")
async def analyze_code_endpoint(payload: CodeInput):
    """Kod analizi endpoint'i"""
    if not payload.code or len(payload.code.strip()) == 0:
        raise HTTPException(status_code=400, detail="Kod içeriği boş olamaz.")

    try:
        analysis_result = analyze_code_with_gemini(payload.code)
        # Sonucu ve kodu veritabanına kaydet
        save_analysis(payload.code, analysis_result)
        return {"analysis": analysis_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analiz sırasında bir hata oluştu: {str(e)}")

@app.get("/api/history")
async def get_analysis_history():
    """Analiz geçmişini döner"""
    try:
        history = get_history()
        # Veritabanından gelen tuple'ları dict'e çevir
        history_list = []
        for item in history:
            history_list.append({
                "id": item[0],
                "timestamp": item[1],
                "original_code": item[2],
                "analysis_result": item[3]
            })
        return history_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geçmiş yüklenirken hata oluştu: {str(e)}")

@app.delete("/api/history/{analysis_id}")
async def delete_single_analysis(analysis_id: int):
    """Tek bir analizi sil"""
    try:
        success = delete_analysis(analysis_id)
        if success:
            return {"message": "Analiz başarıyla silindi"}
        else:
            raise HTTPException(status_code=404, detail="Analiz bulunamadı")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Silme işlemi sırasında hata oluştu: {str(e)}")

@app.delete("/api/history")
async def delete_all_analysis_history():
    """Tüm analizleri sil"""
    try:
        deleted_count = delete_all_analyses()
        return {"message": f"{deleted_count} analiz başarıyla silindi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Silme işlemi sırasında hata oluştu: {str(e)}")

@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {"status": "healthy", "service": "Kod Gözcüsü"}