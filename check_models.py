import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1beta'})

print("🔍 사용 가능한 모델 목록 조회 중...")
try:
    # 모델 목록을 가져와서 'generateContent' 기능이 있는 모델만 출력
    for m in client.models.list():
        if "generateContent" in m.supported_actions:
            print(f"✅ 발견: {m.name}")
except Exception as e:
    print(f"❌ 목록 조회 실패: {e}")