# Portrait Manager (초상화 관리자)

## 한글 설명
초상화 관리자는 BOD 초상화 파일을 쉽게 관리하고 교체할 수 있는 도구입니다.

### 주요 기능
- 현재 초상화와 새 초상화를 나란히 표시
- 썸네일 미리보기 지원
- 파일명 기반 검색 기능
- 자동 백업 시스템
- 624x804 크기 제한 자동 확인
- 한글/영어 언어 지원

### 사용 방법
1. '현재 초상화 폴더 선택' 버튼을 클릭하여 현재 사용 중인 초상화 폴더를 선택합니다.
2. '새 초상화 폴더 선택' 버튼을 클릭하여 교체할 초상화가 있는 폴더를 선택합니다.
3. 각 목록에서 교체하고자 하는 초상화들을 선택합니다.
4. '초상화 교체' 버튼을 클릭하여 교체를 진행합니다.
5. 이전 초상화는 자동으로 backup 폴더에 저장됩니다.

### 주의사항
- .bmp 형식의 파일만 지원됩니다
- 이미지 크기는 624x804 픽셀 이하여야 합니다
- 원본 파일은 자동으로 backup 폴더에 백업됩니다

### 개발 환경
- Python 3.8 이상
- PyQt5
- Pillow (PIL)

### 오픈 소스
이 프로젝트는 Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0) 하에 배포됩니다.

#### 기여 방법
1. 이 저장소를 포크(Fork)합니다.
2. 새로운 기능을 추가하거나 버그를 수정합니다.
3. 변경사항을 커밋하고 풀 리퀘스트(Pull Request)를 보냅니다.

#### 라이선스
Copyright (c) 2024 김진하 (Jinha Kim)

이 프로젝트는 CC BY-NC 4.0 라이선스에 따라 배포됩니다:

1. 저작자 표시 (BY)
   - 이 소프트웨어를 사용, 수정, 또는 배포할 경우 반드시 원작자의 이름(김진하 or JinhaKim or JinhaHyong)을 명시해야 합니다.

2. 비영리 (NC)
   - 이 소프트웨어는 비상업적 목적으로만 사용할 수 있습니다.
   - 상업적 사용은 엄격히 금지됩니다.

3. 기타
   - 이 소프트웨어는 "있는 그대로" 제공되며, 어떠한 형태의 보증도 제공되지 않습니다.
   - 전체 라이선스 내용: https://creativecommons.org/licenses/by-nc/4.0/

---

## English Description
Portrait Manager is a tool for easily managing and replacing BOD portrait files.

### Main Features
- Side-by-side display of current and new portraits
- Thumbnail preview support
- Filename-based search functionality
- Automatic backup system
- 624x804 size limit auto-check
- Korean/English language support

### How to Use
1. Click 'Select Current Portrait Folder' to choose the folder containing current portraits.
2. Click 'Select New Portrait Folder' to choose the folder containing replacement portraits.
3. Select the portraits you want to replace from each list.
4. Click 'Replace Portrait' to proceed with the replacement.
5. Previous portraits are automatically saved in the backup folder.

### Important Notes
- Only .bmp format files are supported
- Image size must be 624x804 pixels or smaller
- Original files are automatically backed up in the backup folder

### Development Environment
- Python 3.8 or higher
- PyQt5
- Pillow (PIL)

### Open Source
This project is distributed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

#### How to Contribute
1. Fork this repository
2. Add new features or fix bugs
3. Commit your changes and send a Pull Request

#### License
Copyright (c) 2024 김진하 (Jinha Kim)

This project is licensed under CC BY-NC 4.0:

1. Attribution (BY)
   - Any use, modification, or distribution of this software must include attribution to the original author (김진하 or JinhaKim or JinhaHyong).

2. NonCommercial (NC)
   - This software may be used for non-commercial purposes only.
   - Commercial use is strictly prohibited.

3. Additional Terms
   - This software is provided "as is" without any form of warranty.
   - Full license text: https://creativecommons.org/licenses/by-nc/4.0/
