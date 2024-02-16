# 정간보 편집기 ([English version](https://github.com/depth221/Jeongganbo-editor/blob/main/README_en.md))
<img src="https://raw.githubusercontent.com/depth221/Jeongganbo-editor/main/README_images/app.png" alt="실행 이미지" width="500">
 
 ## 다운로드
[https://github.com/depth221/Jeongganbo-editor/releases/](https://github.com/depth221/Jeongganbo-editor/releases/)

※ macOS 및 Linux에서는 `pip install jgb-editor`로 정간보 편집기를 설치할 수 있습니다.     
※ macOS에서 실행 파일을 만들려면 아래 '직접 설치' 단락을 참고하세요.

## 소개
지금까지 출시된 정간보 편집기는 2007년에 모젼스랩, 전남대, 단국대에서 공동으로 출시한 [**정간보 매니아**](https://blog.naver.com/jgb_mania/40041295964)와 한 개인 개발자가 2011년 경에 제작한 **정간보 프로젝트**가 있습니다.

다만 정간보 매니아는 업데이트가 끊어진 탓에 윈도우 10 이상의 최신 운영체제를 지원하지 않습니다. 그리고 전문가용 버전은 유료로 판매했으나, 현재는 공식적으로 전문가용 버전을 구매할 방법이 없습니다.

정간보 프로젝트 또한 최근에 다운로드 링크가 사라져 공식적으로 구할 방법이 없어졌습니다.

결국 현재는 정간보를 그릴 때 별도의 채보 프로그램을 쓰기보다는 워드프로세서(한컴오피스 한글, MS 워드 등)를 사용하는 경우가 많아졌습니다. 워드프로세서로 정간보를 그리는 작업은 그리 어렵지 않지만, 각종 시김새나 장식음 이미지 파일을 따로 구해서 삽입해 주어야 한다는 문제점이 있습니다.

이러한 상황에서 워드프로세서를 사용하는 것보다 빠르고, 시김새 그림 파일을 따로 준비할 필요도 없고, 윈도우 외의 운영체제에서도 사용할 수 있는 간단한 **정간보 편집기**를 만들어 보았습니다.

기존 정간보 사보 프로그램에 비해 부족한 부분도 많으나, 이용하면서 불편했던 부분이나 개선점을 이야기해 주시면 최대한 반영하도록 하겠습니다.

## 사용법
### 새로운 정간보 쪽 만들기
![새로운 정간보 쪽 만들기](https://raw.githubusercontent.com/depth221/Jeongganbo-editor/main/README_images/new_page.png)    
`Ctrl+N`으로 정간보 쪽 양식을 새롭게 만들 수 있습니다.
여기에서 '한 페이지에 들어갈 각', '한 각에 들어갈 강', '한 강에 들어갈 정간'을 설정할 수 있으며, 현재로서는 정간보 작성 중 이 설정을 바꿀 수 없습니다.

### 음표 및 쉼표 입력
![국악 음률](https://raw.githubusercontent.com/depth221/Jeongganbo-editor/main/README_images/notes.png)    
각 음은 1~5번 키에 할당되어 있고, 숫자 키를 Ctrl 키와 함께 누르면 하나 높은 음이, Alt 키와 함께 누르면 하나 낮은 음이 입력됩니다. 

`1`: 황종(黃)    
`Ctrl+1`, `Alt+2`: 대려(大)     
`2`: 태주(太)     
`Ctrl+2`: 협종(夾)    
`Alt+3`: 고선(姑)    
`3`: 중려(仲)     
`Ctrl+3`, `Alt+4`: 유빈(蕤)    
`4`: 임종(林)    
`Ctrl+4`: 이칙(夷)    
`Alt+5`: 남려(南)    
`5`: 무역(無)    
`Ctrl+5`, `Alt+1`: 응종(應)    

\` 키(물결표 키)를 누르면 입력되는 음이 한 옥타브 올라간 상태로 고정되며, Shift+\` 키를 누르면 한 옥타브 내려간 상태로 고정됩니다. -2~2옥타브까지 지원합니다.

`-` 키로 연음을 입력할 수 있으며, `space`로 쉼표(△)를 입력할 수 있습니다.

`delete` 키로 클릭된 칸의 내용을 지울 수 있으며, `backspace` 키로 칸 자체를 없앨 수 있습니다.

### 장식음 입력
클릭한 칸에서 마우스 우클릭을 하면 장식음 입력 목록이 나옵니다. 여기서 입력할 장식음을 고를 수 있습니다.

### 새로운 칸 넣기
연속해서 음표를 입력하면 1박~6박에 맞게 칸이 자동으로 조절됩니다. 만약 원하는 형태로 음표를 넣고 싶다면 아래와 같이 직접 칸의 모양을 설정할 수 있습니다.

![현재 칸 오른쪽에 새로운 칸을 만든 모습](https://raw.githubusercontent.com/depth221/Jeongganbo-editor/main/README_images/kan_right.png)    
`Ctrl+→` 키를 누르면 현재 클릭된 칸 오른쪽에 새로운 칸을 만듭니다.

![현재 칸 아래쪽에 새로운 칸을 만든 모습](https://raw.githubusercontent.com/depth221/Jeongganbo-editor/main/README_images/kan_down.png)    
`Ctrl+space` 키를 누르면 현재 클릭된 칸 아래쪽에 새로운 칸을 만듭니다.

### 숨표 입력
![숨표를 입력한 모습](https://raw.githubusercontent.com/depth221/Jeongganbo-editor/main/README_images/sumpyo.png)    
정간 오른쪽 빈 공간의 왼쪽 부분을 클릭하면 숨표가 입력됩니다. 한 번 더 누르면 없어집니다.

### 시김새 입력
![시김새를 입력한 모습](https://raw.githubusercontent.com/depth221/Jeongganbo-editor/main/README_images/sigimsae.png)    
정간 오른쪽 빈 공간의 오른쪽 부분을 클릭하면 시김새를 입력하는 창이 뜹니다. 여기서 원하는 시김새를 입력할 수 있습니다. 버튼을 연속해서 누르면 시김새가 주르륵 입력됩니다.

### 제목-소제목 및 작가 수정
![제목-소제목 및 작가 수정란](https://raw.githubusercontent.com/depth221/Jeongganbo-editor/main/README_images/title_edit.png)    
페이지 오른쪽의 제목 및 소제목 부분을 클릭하면 위와 같이 제목 및 작가를 수정할 수 있습니다.

### 페이지 넘기기
이전 페이지로 넘어가려면 `Page Up`(`PgUp`) 키, 다음 페이지로 넘어가려면 `Page Down`(`PgDn`) 키를 누르면 됩니다.    
또한 정간보를 작성하다가 페이지의 끝에 도달하면 자동으로 다음 페이지로 넘어갑니다.

### 저장 / 열기
`Ctrl+S`로 정간보 프로젝트 파일(.jgbx)을 저장합니다(이미지 파일이 아님!). `Ctrl+O`로 저장해 놓은 프로젝트 파일을 불러올 수 있습니다.

### 내보내기
`Ctrl+E`로 정간보를 이미지(.png) 파일로 내보낼 수 있습니다. 각 페이지마다 한 장의 이미지 파일로 저장됩니다.

## 악보 예시
정간보 예시 파일은 [example](https://github.com/depth221/Jeongganbo-editor/tree/main/example) 폴더에 있습니다.

## 직접 설치
### 의존성
* Python 3.10
* PyQt5
* BeautifulSoap
* pyinstaller(실행 파일로 만들 시에만)

### 윈도우
※ pip을 먼저 설치해야 합니다!
```powershell
pip install -r requirement.txt
.\make_exe.cmd
```

실행 파일은 `dist` 폴더에 있습니다.


### 맥
※ 기본적으로 최근 macOS에는 pip3가 기본적으로 설치되어 있습니다. 만약 pip3가 설치되어 있지 않다면 [파이썬 공식 웹 사이트](https://www.python.org/downloads/macos/)에서 macOS용 파이썬을 설치해 주세요.
```bash
pip3 install -r requirement.txt
./make_exe.sh
```

실행
```bash
./dist/jeongganbo_editor/jeongganbo_editor
```

### 리눅스
```bash
sudo apt install pip
pip install -r requirement.txt
./make_exe.sh
```

실행
```bash
./dist/jeongganbo_editor/jeongganbo_editor
```

## 구현 예정
[ ] 번역 개선    
[ ] 테마(글꼴, 배경색 등) 변경 기능 추가   
[ ] 정간보 매니아 파일(.jgb) 부분 지원(공개 포맷이 아니라 완전 지원은 어렵습니다)    
[ ] 미디(MIDI) 재생 기능 추가    
[ ] PDF로 정간보 내보내기 기능 추가