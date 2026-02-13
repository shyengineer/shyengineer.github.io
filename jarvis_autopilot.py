import os
import time
import re
import schedule
from datetime import datetime
from io import BytesIO

# --- 라이브러리 로드 ---
try:
    from dotenv import load_dotenv
    from google import genai
    from google.genai import types
    from git import Repo
    from PIL import Image
except ImportError as e:
    print(f"❌ 필수 라이브러리 누락: {e}")
    print("💡 팁: pip install google-genai gitpython pillow schedule python-dotenv")
    exit()

# --- [설정 구간] ---
load_dotenv() # .env 파일에서 환경변수 로드
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ 오류: .env 파일에 GOOGLE_API_KEY가 없습니다.")
    exit()

# 경로를 절대 경로로 설정하여 어디서 실행하든 안전하게 만듦
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_ROOT = BASE_DIR                     
POSTS_DIR = os.path.join(BLOG_ROOT, "content", "posts")          
IMAGES_DIR = os.path.join(BLOG_ROOT, "static", "images")         
SCHEDULE_TIME = "09:00" 

# 클라이언트 초기화
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1beta'})

def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🤖 자비스: {message}")

def safe_generate_content(prompt, model_candidates=["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-2.5-flash"], max_retries=3):
    """
    업데이트된 모델 목록 적용: Lite 모델 우선 사용으로 할당량 절약
    """
    for attempt in range(max_retries):
        # log(f"🔄 시도 {attempt+1}/{max_retries} 진입...") 
        
        for model_name in model_candidates:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text
                
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    log(f"⚠️ [{model_name}] 할당량 초과. 즉시 다음 모델로 넘어갑니다.")
                    continue 
                elif "404" in error_msg:
                    log(f"⚠️ [{model_name}] 모델을 찾을 수 없습니다.")
                    continue
                else:
                    log(f"❌ 오류 발생 ({model_name}): {e}")
                    time.sleep(5) 
        
        log(f"💤 모든 모델이 바쁩니다. 60초 휴식 후 다시 시도합니다...")
        time.sleep(60)
    
    return None

def get_trending_topic():
    log("트렌드 분석 중...")
    prompt = """
    Act as a Tech Trend Analyst.
    Suggest ONE specific, profitable blog topic related to:
    "Semiconductor Physics, AI Engineering, or Quantitative Economics".
    Output ONLY the topic title in Korean.
    Example: 3나노 공정의 수율 문제와 경제적 영향
    """
    topic = safe_generate_content(prompt)
    return topic.strip() if topic else "인공지능과 반도체의 미래"

def generate_blog_content(topic):
    log(f"'{topic}' 원고 작성 시작...")
    prompt = f"""
    Write a professional tech blog post in **Korean** about: "{topic}".
    **Role**: You are 'ShyEngineer'.
    **Structure**:
    1. **Front Matter**: Hugo format.
       - title: "{topic}"
       - date: {datetime.now().strftime("%Y-%m-%d")}
       - categories: [Engineering]
       - tags: [Tech, Economics]
       - author: "ShyEngineer"
    2. **Content**: High technical depth, Markdown format.
    3. **Image Prompt**: Include [IMAGE_PROMPT: English description] at the top.
    """
    return safe_generate_content(prompt)

def extract_image_prompt(content):
    if not content: return "Tech background"
    match = re.search(r"\[IMAGE_PROMPT:\s*(.*?)\]", content)
    return match.group(1) if match else "Futuristic high tech background, 8k"

def generate_and_save_webp(prompt, filename_base):
    log(f"이미지 생성 요청 중...")
    
    # [수정] 모델 이름을 사용 가능한 모델로 변경
    # 사용자 목록에 있던 'gemini-2.0-flash-exp' 사용
    image_model = 'gemini-2.0-flash-exp' 
    
    try:
        response = client.models.generate_images(
            model=image_model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                output_mime_type="image/png"
            )
        )
        
        for generated_image in response.generated_images:
            image_bytes = generated_image.image.image_bytes
            img = Image.open(BytesIO(image_bytes))
            
            save_path = os.path.join(IMAGES_DIR, f"{filename_base}.webp")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            img.save(save_path, "webp", quality=80)
            log(f"✅ 이미지 저장 완료: {save_path}")
            return f"/images/{filename_base}.webp"
            
    except Exception as e:
        log(f"⚠️ 이미지 생성 실패 (건너뜀): {e}")
        return None

def save_file_and_deploy(topic, content, image_rel_path):
    safe_title = re.sub(r'[^\w\s-]', '', topic).strip().replace(" ", "-").lower()
    filename = f"{datetime.now().strftime('%Y-%m-%d')}-{safe_title}.md"
    file_path = os.path.join(POSTS_DIR, filename)
    
    # 이미지 경로 삽입 및 프롬프트 제거
    if image_rel_path:
        content = content.replace("draft: false", f"draft: false\r\ncover:\r\n  image: {image_rel_path}")
        content = re.sub(r"\[IMAGE_PROMPT:.*?\]", "", content)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"📄 파일 저장: {filename}")

    try:
        repo = Repo(BLOG_ROOT)
        # 배포 전 Pull을 먼저 하여 충돌 방지 (선택 사항)
        # repo.remotes.origin.pull() 
        repo.git.add(all=True)
        repo.index.commit(f"Auto-post: {topic}")
        repo.remotes.origin.push()
        log("🚀 GitHub Push 완료!")
    except Exception as e:
        log(f"❌ Git 배포 실패: {e}")

def run_automation_cycle():
    print("\n" + "="*50)
    log("🚀 [자비스 v5.1] 작업 시작")
    topic = get_trending_topic()
    content = generate_blog_content(topic)
    
    if content:
        img_prompt = extract_image_prompt(content)
        safe_title = re.sub(r'[^\w\s-]', '', topic).strip().replace(" ", "-").lower()
        image_rel_path = generate_and_save_webp(img_prompt, safe_title)
        save_file_and_deploy(topic, content, image_rel_path)
    
    print("="*50 + "\n")

if __name__ == "__main__":
    print("⚡ 자비스 시스템 가동 (수정판) ⚡")
    
    # [수정] 아래 줄의 #을 지워주세요!
    run_automation_cycle() 
    
    # 그 다음 스케줄러 실행
    schedule.every().day.at(SCHEDULE_TIME).do(run_automation_cycle)
    
    while True:
        schedule.run_pending()
        time.sleep(60)