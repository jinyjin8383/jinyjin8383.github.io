import os
import re

# 경로 설정 (압축 풀린 폴더 기준으로 수정하세요)
BASE_DIR = "extracted"   # <- 여기를 본인 경로로 수정
CSS_PATH = os.path.join(BASE_DIR, "resources/css/main.css")

# HTML 파일 모두 수집
html_files = []
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

# main.css 읽기
with open(CSS_PATH, "r", encoding="utf-8", errors="ignore") as f:
    css_text = f.read()

# CSS 내 클래스, 아이디 선택자 추출
css_classes = set(re.findall(r'\.([\w\-]+)', css_text))
css_ids = set(re.findall(r'#([\w\-]+)', css_text))

# HTML 내 실제 사용된 클래스/아이디 추출
html_classes = set()
html_ids = set()

for path in html_files:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
        # class 속성 추출
        for classes in re.findall(r'class="([^"]+)"', html):
            for c in classes.split():
                html_classes.add(c.strip())
        # id 속성 추출
        for ids in re.findall(r'id="([^"]+)"', html):
            html_ids.add(ids.strip())

# 사용되지 않은 CSS 선택자 추출
unused_classes = css_classes - html_classes
unused_ids = css_ids - html_ids

print("=== 결과 ===")
print(f"전체 CSS 클래스 수: {len(css_classes)}")
print(f"전체 CSS 아이디 수: {len(css_ids)}")
print(f"안 쓰는 클래스 수: {len(unused_classes)}")
print(f"안 쓰는 아이디 수: {len(unused_ids)}\n")

print("안 쓰는 클래스 목록:")
print(sorted(unused_classes))

print("\n안 쓰는 아이디 목록:")
print(sorted(unused_ids))
