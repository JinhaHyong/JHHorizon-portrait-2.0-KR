from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QLabel, QFileDialog, QWidget, QMessageBox,
                            QFrame, QScrollArea, QGridLayout, QLineEdit, QDialogButtonBox, QLayout, QDialog,
                            QDesktopWidget)
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSlot
from PIL import Image
import os
import sys
import shutil
import time

class PhotoManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("[BOD] JHHorizon 초상화 교체 프로그램 2.0")
        
        # 아이콘 설정
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "아이콘.ico")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self.setWindowIcon(icon)
        
        # 배경색 설정
        self.setStyleSheet("background-color: white;")
        
        # 크기 변경 이벤트 연결
        self.resizeEvent = self.on_resize
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 버튼 스타일
        button_style = """
            QPushButton {
                background-color: #1E3D59;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-family: '맑은 고딕';
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #2E4D69;
            }
        """
        
        # 좌우 레이아웃 생성
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)
        
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        
        # 좌측 영역
        self.current_folder_btn = QPushButton("현재 초상화 폴더 선택")
        self.current_folder_btn.setStyleSheet(button_style)
        self.current_folder_btn.clicked.connect(self.load_current_folder)
        self.current_folder_btn.setFixedWidth(400)
        left_layout.addWidget(self.current_folder_btn, alignment=Qt.AlignCenter)
        
        # 현재 초상화 목록
        current_list_frame = QFrame()
        current_list_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        current_list_frame.setStyleSheet("QFrame { border: 1px solid #ddd; background-color: white; }")
        current_list_layout = QVBoxLayout(current_list_frame)
        current_list_layout.setContentsMargins(10, 10, 10, 10)
        current_list_layout.setSpacing(5)
        
        current_title = QLabel("현재 초상화 목록")
        current_title.setFont(QFont("맑은 고딕", 9))
        current_title.setStyleSheet("padding: 0px; margin: 0px; border: none;")
        current_title.setStyleSheet("border: none;")
        current_list_layout.addWidget(current_title)
        
        self.current_scroll = QScrollArea()
        self.current_scroll.setWidgetResizable(True)
        self.current_scroll.setStyleSheet("background-color: white;")
        current_list_layout.addWidget(self.current_scroll)
        
        self.current_grid = QWidget()
        self.current_grid.setStyleSheet("background-color: white;")
        self.current_grid_layout = QGridLayout(self.current_grid)
        self.current_grid_layout.setSpacing(5)
        self.current_scroll.setWidget(self.current_grid)
        
        current_list_frame.setFixedWidth(400)
        current_list_frame.setFixedHeight(400)
        left_layout.addWidget(current_list_frame)
        
        # 현재 초상화 미리보기
        current_preview_container = QFrame()
        current_preview_container.setFrameStyle(QFrame.StyledPanel)
        current_preview_container.setFixedWidth(400)
        current_preview_container.setFixedHeight(400)
        current_preview_layout = QVBoxLayout(current_preview_container)
        current_preview_layout.setContentsMargins(10, 10, 10, 10)
        current_preview_layout.setSpacing(5)
        
        current_preview_title = QLabel("현재 초상화 미리보기")
        current_preview_title.setFont(QFont("맑은 고딕", 9))
        current_preview_title.setAlignment(Qt.AlignCenter)
        current_preview_title.setStyleSheet("padding: 0px; margin: 0px;")
        current_preview_layout.addWidget(current_preview_title)
        
        self.current_preview_label = QLabel()
        self.current_preview_label.setAlignment(Qt.AlignCenter)
        self.current_preview_label.setMinimumSize(380, 350)
        self.current_preview_label.setMaximumSize(380, 350)
        current_preview_layout.addWidget(self.current_preview_label)
        
        # 미리보기 중앙 정렬을 위한 컨테이너
        preview_wrapper = QWidget()
        preview_wrapper_layout = QHBoxLayout(preview_wrapper)
        preview_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        preview_wrapper_layout.addStretch()
        preview_wrapper_layout.addWidget(current_preview_container)
        preview_wrapper_layout.addStretch()
        left_layout.addWidget(preview_wrapper)
        
        # 우측 영역
        self.new_folder_btn = QPushButton("새 초상화 폴더 선택")
        self.new_folder_btn.setStyleSheet(button_style)
        self.new_folder_btn.clicked.connect(self.select_new_folder)
        self.new_folder_btn.setFixedWidth(400)
        right_layout.addWidget(self.new_folder_btn, alignment=Qt.AlignCenter)
        
        # 새 초상화 목록
        new_list_frame = QFrame()
        new_list_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        new_list_frame.setStyleSheet("QFrame { border: 1px solid #ddd; background-color: white; }")
        new_list_layout = QVBoxLayout(new_list_frame)
        new_list_layout.setContentsMargins(10, 10, 10, 10)
        new_list_layout.setSpacing(5)
        
        # 제목과 검색창을 위한 컨테이너
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 5)
        header_layout.setSpacing(5)
        
        new_title = QLabel("새 초상화 목록")
        new_title.setFont(QFont("맑은 고딕", 9))
        new_title.setStyleSheet("padding: 0px; margin: 0px; border: none;")
        new_title.setStyleSheet("border: none;")
        header_layout.addWidget(new_title)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("이미지 이름 검색...")
        self.search_input.setStyleSheet("QLineEdit { padding: 3px; font: 9pt '맑은 고딕'; }")
        self.search_input.textChanged.connect(self.filter_thumbnails)
        header_layout.addWidget(self.search_input)
        
        new_list_layout.addWidget(header_container)
        
        self.new_scroll = QScrollArea()
        self.new_scroll.setWidgetResizable(True)
        self.new_scroll.setStyleSheet("background-color: white;")
        new_list_layout.addWidget(self.new_scroll)
        
        self.new_grid = QWidget()
        self.new_grid.setStyleSheet("background-color: white;")
        self.new_grid_layout = QGridLayout(self.new_grid)
        self.new_grid_layout.setSpacing(5)
        self.new_scroll.setWidget(self.new_grid)
        
        new_list_frame.setFixedWidth(400)
        new_list_frame.setFixedHeight(400)
        right_layout.addWidget(new_list_frame)
        
        # 새 초상화 미리보기
        new_preview_container = QFrame()
        new_preview_container.setFrameStyle(QFrame.StyledPanel)
        new_preview_container.setFixedWidth(400)
        new_preview_container.setFixedHeight(400)
        new_preview_layout = QVBoxLayout(new_preview_container)
        new_preview_layout.setContentsMargins(10, 10, 10, 10)
        new_preview_layout.setSpacing(5)
        
        new_preview_title = QLabel("새 초상화 미리보기")
        new_preview_title.setFont(QFont("맑은 고딕", 9))
        new_preview_title.setAlignment(Qt.AlignCenter)
        new_preview_title.setStyleSheet("padding: 0px; margin: 0px;")
        new_preview_layout.addWidget(new_preview_title)
        
        self.new_preview_label = QLabel()
        self.new_preview_label.setAlignment(Qt.AlignCenter)
        self.new_preview_label.setMinimumSize(380, 350)
        self.new_preview_label.setMaximumSize(380, 350)
        new_preview_layout.addWidget(self.new_preview_label)
        
        # 미리보기 중앙 정렬을 위한 컨테이너
        new_preview_wrapper = QWidget()
        new_preview_wrapper_layout = QHBoxLayout(new_preview_wrapper)
        new_preview_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        new_preview_wrapper_layout.addStretch()
        new_preview_wrapper_layout.addWidget(new_preview_container)
        new_preview_wrapper_layout.addStretch()
        right_layout.addWidget(new_preview_wrapper)
        
        # 언어 선택 버튼
        lang_container = QWidget()
        lang_layout = QHBoxLayout(lang_container)
        lang_layout.setContentsMargins(0, 0, 0, 0)
        lang_layout.setSpacing(0)
        
        # 언어 선택 버튼 스타일
        lang_button_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                padding: 2px;
                font-size: 8pt;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked {
                background-color: #d0d0d0;
            }
        """
        
        self.kr_btn = QPushButton("한국어")
        self.kr_btn.setFixedWidth(43)
        self.kr_btn.setStyleSheet(lang_button_style)
        self.kr_btn.setCheckable(True)
        self.kr_btn.setChecked(True)
        self.kr_btn.clicked.connect(self.change_language)
        
        self.en_btn = QPushButton("EN")
        self.en_btn.setFixedWidth(43)
        self.en_btn.setStyleSheet(lang_button_style)
        self.en_btn.setCheckable(True)
        self.en_btn.clicked.connect(self.change_language)
        
        lang_layout.addWidget(self.kr_btn)
        lang_layout.addWidget(self.en_btn)
        
        # 좌우 레이아웃 추가
        content_layout.addLayout(left_layout)
        content_layout.addLayout(right_layout)
        
        # 하단 레이아웃 설정
        bottom_container = QWidget()
        bottom_container.setFixedHeight(35)
        bottom_layout = QHBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(10, 0, 10, 0)
        bottom_layout.setSpacing(2)
        
        # 왼쪽 영역 (제작자/길드 정보)
        info_container = QWidget()
        info_layout = QHBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)
        
        self.creator_label = QLabel("제작자 : 귀물(진하형)")
        self.creator_label.setStyleSheet("color: blue; font-family: '맑은 고딕'; font-size: 8pt;")
        info_layout.addWidget(self.creator_label)
        
        self.separator_label = QLabel(" /")  
        self.separator_label.setStyleSheet("font-family: '맑은 고딕'; font-size: 8pt;")
        info_layout.addWidget(self.separator_label)
        
        self.guild_label = QLabel(" 길드 : 노블레스")  
        self.guild_label.setStyleSheet("color: red; font-family: '맑은 고딕'; font-size: 8pt;")
        info_layout.addWidget(self.guild_label)
        
        # 중앙 영역 (초상화 교체 버튼)
        center_container = QWidget()
        center_layout = QHBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        
        self.replace_button = QPushButton("초상화 교체")
        self.replace_button.setFixedWidth(120)
        self.replace_button.setStyleSheet(button_style)
        self.replace_button.clicked.connect(self.replace_photo)
        
        center_layout.addStretch()
        center_layout.addWidget(self.replace_button)
        center_layout.addStretch()
        
        # 오른쪽 영역 (언어 선택 버튼)
        lang_container = QWidget()
        lang_layout = QHBoxLayout(lang_container)
        lang_layout.setContentsMargins(0, 0, 0, 0)
        lang_layout.setSpacing(0)
        
        # 언어 선택 버튼 스타일
        lang_button_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                padding: 2px;
                font-size: 8pt;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked {
                background-color: #d0d0d0;
            }
        """
        
        self.kr_btn = QPushButton("한국어")
        self.kr_btn.setFixedWidth(43)
        self.kr_btn.setStyleSheet(lang_button_style)
        self.kr_btn.setCheckable(True)
        self.kr_btn.setChecked(True)
        self.kr_btn.clicked.connect(self.change_language)
        
        self.en_btn = QPushButton("EN")
        self.en_btn.setFixedWidth(43)
        self.en_btn.setStyleSheet(lang_button_style)
        self.en_btn.setCheckable(True)
        self.en_btn.clicked.connect(self.change_language)
        
        lang_layout.addWidget(self.kr_btn)
        lang_layout.addWidget(self.en_btn)
        
        # 하단 레이아웃에 위젯 추가 (1:2:1 비율)
        bottom_layout.addWidget(info_container, 1)
        bottom_layout.addWidget(center_container, 2)
        bottom_layout.addWidget(lang_container, 1, Qt.AlignRight)  # 오른쪽 정렬
        
        # 메인 레이아웃에 추가
        main_layout.addLayout(content_layout)
        main_layout.addWidget(bottom_container)
        
        # 메인 위젯 설정
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # 창 크기 고정
        self.setFixedSize(830, 910)
        
        # 창을 화면 중앙으로 이동
        center = QDesktopWidget().availableGeometry().center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        
        # 기본 초상화 경로 설정 및 목록 불러오기
        self.photo_path = os.path.join(os.path.expanduser("~"), "Documents", "Black Desert", "FaceTexture")
        if os.path.exists(self.photo_path):
            try:
                self.load_thumbnails(self.photo_path, self.current_grid_layout)
            except Exception as e:
                self.show_warning(f"기본 초상화 폴더를 불러오는 중 오류가 발생했습니다: {str(e)}")
        else:
            # 경로가 없으면 사용자에게 알림
            self.show_info("기본 초상화 경로를 찾을 수 없습니다.\n'현재 초상화 폴더 선택' 버튼을 눌러 수동으로 선택해주세요.")
        
        # 초기화
        self.current_photo = None
        self.new_photo = None
        self.current_selected_label = None
        self.new_selected_label = None
        
        # 초기 경로 설정
        self.new_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "새 초상화")
        
        # 초기 썸네일 로드
        if os.path.exists(self.new_path):
            try:
                self.load_thumbnails(self.new_path, self.new_grid_layout)
            except Exception as e:
                self.show_warning(f"새 초상화 폴더를 불러오는 중 오류가 발생했습니다: {str(e)}")

        self.current_language = 'kr'  # 기본 언어 설정
        
    def load_current_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "현재 초상화 폴더 선택")
        if folder:
            self.photo_path = folder
            # 선택 상태 초기화
            self.current_selected_label = None
            self.current_photo = None
            self.current_preview_label.clear()
            # 기존 썸네일 제거
            self.clear_layout(self.current_grid_layout)
            # 새 썸네일 로드
            try:
                self.load_thumbnails(folder, self.current_grid_layout)
            except Exception as e:
                self.show_warning(f"현재 초상화 폴더를 불러오는 중 오류가 발생했습니다: {str(e)}")

    def select_new_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "새 초상화 폴더 선택")
        if folder:
            # 기존 썸네일 제거
            self.clear_layout(self.new_grid_layout)
            
            # 선택 상태 초기화
            self.new_selected_label = None
            self.new_photo = None
            self.new_preview_label.clear()
            
            # 경로 설정
            self.new_path = folder
            
            # 검색어 초기화 (이벤트 발생 방지)
            self.search_input.blockSignals(True)
            self.search_input.setText("")
            self.search_input.blockSignals(False)
            
            # 썸네일 로드
            self.load_thumbnails(folder, self.new_grid_layout)

    def load_thumbnails(self, folder, grid_layout, filter_text=""):
        try:
            self.clear_layout(grid_layout)
            
            if not os.path.exists(folder):
                return
                
            # .bmp 파일만 필터링
            files = [f for f in os.listdir(folder) if f.lower().endswith('.bmp')]
            
            # 검색어로 필터링
            if filter_text:
                files = [f for f in files if filter_text.lower() in f.lower()]
                
            if not files and not filter_text:  # 검색어가 없을 때만 경고 메시지 표시
                if grid_layout == self.current_grid_layout:
                    self.show_warning("현재 초상화 폴더에 .bmp 형식의 이미지가 없습니다.")
                else:
                    self.show_warning("새 초상화 폴더에 .bmp 형식의 이미지가 없습니다.")
                return
                
            row = 0
            col = 0
            max_cols = 3
            
            valid_files = []
            for file in sorted(files):
                file_path = os.path.join(folder, file)
                try:
                    if not os.path.exists(file_path):
                        continue
                        
                    image = Image.open(file_path)
                    width, height = image.size
                    
                    # 624x804 크기 체크
                    if width > 624 or height > 804:
                        continue
                        
                    valid_files.append((file_path, image))
                        
                except Exception as e:
                    print(f"Error checking image size for {file}: {str(e)}")
                    continue
            
            if not valid_files and not filter_text:  # 검색어가 없을 때만 경고 메시지 표시
                if grid_layout == self.current_grid_layout:
                    self.show_warning("현재 초상화 폴더에 624x804 이하 크기의 .bmp 이미지가 없습니다.")
                else:
                    self.show_warning("새 초상화 폴더에 624x804 이하 크기의 .bmp 이미지가 없습니다.")
                return
            
            for file_path, image in valid_files:
                try:
                    # 썸네일 크기
                    thumbnail_size = (100, 100)
                    
                    # 이미지 비율 계산
                    width, height = image.size
                    ratio = min(thumbnail_size[0] / width, thumbnail_size[1] / height)
                    new_size = (int(width * ratio), int(height * ratio))
                    
                    # 비율 유지하면서 리사이즈
                    image = image.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # 새 이미지 생성 (100x100 흰색 배경)
                    new_image = Image.new('RGB', thumbnail_size, 'white')
                    # 이미지를 중앙에 붙여넣기
                    paste_x = (thumbnail_size[0] - new_size[0]) // 2
                    paste_y = (thumbnail_size[1] - new_size[1]) // 2
                    new_image.paste(image, (paste_x, paste_y))
                    
                    pixmap = self.convert_to_pixmap(new_image)
                    
                    # 썸네일 컨테이너 생성
                    thumbnail_container = QFrame()
                    thumbnail_container.setFixedSize(102, 102)
                    thumbnail_container.setStyleSheet("""
                        QFrame {
                            border: 1px solid #ddd;
                            background-color: white;
                            margin: 0px;
                            padding: 0px;
                        }
                        QFrame:hover {
                            border: 1px solid #aaa;
                        }
                    """)
                    
                    container_layout = QVBoxLayout(thumbnail_container)
                    container_layout.setContentsMargins(1, 1, 1, 1)
                    container_layout.setSpacing(0)
                    
                    # 이미지 레이블
                    thumbnail_label = QLabel()
                    thumbnail_label.setPixmap(pixmap.scaled(98, 98, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    thumbnail_label.setAlignment(Qt.AlignCenter)
                    thumbnail_label.setFixedSize(98, 98)
                    thumbnail_label.setStyleSheet("""
                        QLabel {
                            border: none;
                            background-color: white;
                            margin: 0px;
                            padding: 0px;
                        }
                    """)
                    container_layout.addWidget(thumbnail_label)
                    
                    # 파일 경로를 위젯의 속성으로 저장
                    thumbnail_container.file_path = file_path
                    
                    # 클릭 이벤트 설정
                    is_current = (grid_layout == self.current_grid_layout)
                    thumbnail_container.mousePressEvent = lambda e, path=file_path, current=is_current, container=thumbnail_container: self.thumbnail_clicked(path, current, container)
                    
                    grid_layout.addWidget(thumbnail_container, row, col)
                    
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                        
                except Exception as e:
                    print(f"Error loading thumbnail for {file_path}: {str(e)}")
                    continue
                    
        except Exception as e:
            self.show_warning(f"썸네일을 불러오는 중 오류가 발생했습니다: {str(e)}")

    def filter_thumbnails(self):
        if not self.new_path:
            return
        search_text = self.search_input.text()
        self.load_thumbnails(self.new_path, self.new_grid_layout, search_text)

    def thumbnail_clicked(self, image_path, is_current, clicked_widget):
        try:
            if not os.path.exists(image_path):
                self.show_warning("선택한 이미지 파일을 찾을 수 없습니다.")
                return
            
            # 이전 선택 상태의 스타일 초기화
            if is_current and self.current_selected_label:
                try:
                    old_widget = self.current_selected_label
                    if old_widget and old_widget != clicked_widget:
                        old_widget.setStyleSheet("""
                            QFrame {
                                border: 1px solid #ddd;
                                background-color: white;
                                margin: 0px;
                                padding: 0px;
                            }
                            QFrame:hover {
                                border: 1px solid #aaa;
                            }
                        """)
                except:
                    self.current_selected_label = None
            
            if not is_current and self.new_selected_label:
                try:
                    old_widget = self.new_selected_label
                    if old_widget and old_widget != clicked_widget:
                        old_widget.setStyleSheet("""
                            QFrame {
                                border: 1px solid #ddd;
                                background-color: white;
                                margin: 0px;
                                padding: 0px;
                            }
                            QFrame:hover {
                                border: 1px solid #aaa;
                            }
                        """)
                except:
                    self.new_selected_label = None
            
            # 새로운 선택 상태 설정
            try:
                clicked_widget.setStyleSheet("""
                    QFrame {
                        border: 2px solid #007bff;
                        background-color: white;
                        margin: 0px;
                        padding: 0px;
                    }
                """)
            except:
                print("새로운 선택 상태 설정 실패")
                return
            
            # 미리보기 업데이트
            try:
                image = Image.open(image_path)
                preview_size = (300, 300)
                
                # 이미지 비율 계산
                width, height = image.size
                ratio = min(preview_size[0] / width, preview_size[1] / height)
                new_size = (int(width * ratio), int(height * ratio))
                
                # 비율 유지하면서 리사이즈
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                
                # 새 이미지 생성 (300x300 흰색 배경)
                new_image = Image.new('RGB', preview_size, 'white')
                # 이미지를 중앙에 붙여넣기
                paste_x = (preview_size[0] - new_size[0]) // 2
                paste_y = (preview_size[1] - new_size[1]) // 2
                new_image.paste(image, (paste_x, paste_y))
                
                pixmap = self.convert_to_pixmap(new_image)
                
                if is_current:
                    self.current_preview_label.setPixmap(pixmap)
                    self.current_photo = image_path
                    self.current_selected_label = clicked_widget
                else:
                    self.new_preview_label.setPixmap(pixmap)
                    self.new_photo = image_path
                    self.new_selected_label = clicked_widget
                    
            except Exception as e:
                print(f"미리보기 업데이트 중 오류 발생: {str(e)}")
                
        except Exception as e:
            print(f"썸네일 클릭 처리 중 오류 발생: {str(e)}")

    def convert_to_pixmap(self, image):
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        # 미리보기 영역 크기
        target_width = 350
        target_height = 350
        
        # 원본 이미지 크기
        width, height = image.size
        
        # 비율 계산
        width_ratio = target_width / width
        height_ratio = target_height / height
        ratio = min(width_ratio, height_ratio)
        
        # 새로운 크기 계산
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        # 이미지 리사이즈
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        qimage = QImage(image.tobytes(), image.width, image.height, 3 * image.width, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def replace_photo(self):
        try:
            if not self.current_photo or not self.new_photo:
                self.show_warning("현재 초상화와 새 초상화를 모두 선택해주세요.")
                return
                
            if not os.path.exists(self.current_photo) or not os.path.exists(self.new_photo):
                self.show_warning("선택된 이미지 파일을 찾을 수 없습니다.")
                return
            
            # 현재 초상화 폴더와 파일 정보
            current_dir = os.path.dirname(self.current_photo)
            current_filename = os.path.basename(self.current_photo)
            
            # backup 폴더 생성
            backup_dir = os.path.join(current_dir, "backup")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # 백업 파일명 생성 (현재 시간 추가)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{os.path.splitext(current_filename)[0]}_{timestamp}{os.path.splitext(current_filename)[1]}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 현재 초상화를 백업
            shutil.copy2(self.current_photo, backup_path)
            
            # 현재 초상화를 새 초상화로 덮어씌우기
            shutil.copy2(self.new_photo, self.current_photo)
            
            # 파일 경로 저장
            current_file = self.current_photo
            new_file = self.new_photo
            
            # 현재 검색어 저장
            current_search = self.search_input.text()
            
            # 초상화 교체 후 목록 업데이트 (검색어 유지)
            self.load_thumbnails(self.photo_path, self.current_grid_layout)
            self.load_thumbnails(self.new_path, self.new_grid_layout, current_search)
            
            # 선택 상태 복원
            for i in range(self.current_grid_layout.count()):
                widget = self.current_grid_layout.itemAt(i).widget()
                if widget and hasattr(widget, 'file_path'):
                    if widget.file_path == current_file:
                        widget.setStyleSheet("""
                            QFrame {
                                border: 2px solid #007bff;
                                background-color: white;
                                margin: 0px;
                                padding: 0px;
                            }
                        """)
                        self.current_selected_label = widget
                        break
            
            for i in range(self.new_grid_layout.count()):
                widget = self.new_grid_layout.itemAt(i).widget()
                if widget and hasattr(widget, 'file_path'):
                    if widget.file_path == new_file:
                        widget.setStyleSheet("""
                            QFrame {
                                border: 2px solid #007bff;
                                background-color: white;
                                margin: 0px;
                                padding: 0px;
                            }
                        """)
                        self.new_selected_label = widget
                        break
            
            # 이미지를 다시 로드하여 미리보기 업데이트
            try:
                if os.path.exists(new_file):
                    new_image = Image.open(new_file)
                    new_pixmap = self.convert_to_pixmap(new_image)
                    self.current_preview_label.setPixmap(new_pixmap)
                    self.new_preview_label.setPixmap(new_pixmap)
                    
                    # 현재 파일과 새 파일 경로 유지
                    self.current_photo = current_file
                    self.new_photo = new_file
            except Exception as e:
                print(f"미리보기 업데이트 중 오류 발생: {str(e)}")
            
            # 교체가 완료된 후 메시지 표시
            self.show_info("초상화가 교체되었습니다.\n이전 초상화는 backup 폴더에 저장되었습니다.")
            
        except Exception as e:
            self.show_warning(f"초상화 교체 중 오류가 발생했습니다.\n{str(e)}")

    def on_resize(self, event):
        super().resizeEvent(event)

    def clear_layout(self, layout):
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            if item.layout():
                self.clear_layout(item.layout())

    def change_language(self, checked):
        if not checked:  # 체크 해제된 버튼은 무시
            return
            
        sender = self.sender()
        if sender == self.kr_btn:
            self.setWindowTitle("[BOD] JHHorizon 초상화 교체 2.0")
            self.current_folder_btn.setText("현재 초상화 폴더 선택")
            self.new_folder_btn.setText("새 초상화 폴더 선택")
            self.search_input.setPlaceholderText("이미지 이름 검색...")
            self.replace_button.setText("초상화 교체")
            self.creator_label.setText("제작자 : 귀물(진하형)")
            self.guild_label.setText(" 길드 : 노블레스")
            self.guild_label.setVisible(True)  # 한국어 모드에서는 길드 정보 표시
            self.separator_label.setVisible(True)  # 한국어 모드에서는 구분자 표시
            # 목록과 미리보기 문구 추가
            for label in self.findChildren(QLabel):
                if label.text() == "Current Portrait List" or label.text() == "New Portrait List":
                    label.setText("현재 초상화 목록" if "Current" in label.text() else "새 초상화 목록")
                elif label.text() == "Current Portrait Preview" or label.text() == "New Portrait Preview":
                    label.setText("현재 초상화 미리보기" if "Current" in label.text() else "새 초상화 미리보기")
            self.en_btn.setChecked(False)
            self.current_language = 'kr'
        else:
            self.setWindowTitle("JHHorizon Portrait Replacement Program 2.0")
            self.current_folder_btn.setText("Select Current Portrait Folder")
            self.new_folder_btn.setText("Select New Portrait Folder")
            self.search_input.setPlaceholderText("Search image name...")
            self.replace_button.setText("Replace Portrait")
            self.creator_label.setText("Creator : JinhaHyong")
            self.guild_label.setVisible(False)  # 영어 모드에서는 길드 정보 숨김
            self.separator_label.setVisible(False)  # 영어 모드에서는 구분자 숨김
            # 목록과 미리보기 문구 추가
            for label in self.findChildren(QLabel):
                if label.text() == "현재 초상화 목록" or label.text() == "새 초상화 목록":
                    label.setText("Current Portrait List" if "현재" in label.text() else "New Portrait List")
                elif label.text() == "현재 초상화 미리보기" or label.text() == "새 초상화 미리보기":
                    label.setText("Current Portrait Preview" if "현재" in label.text() else "New Portrait Preview")
            self.kr_btn.setChecked(False)
            self.current_language = 'en'

    def show_warning(self, message):
        # 메시지에 따른 번역 처리
        if self.current_language == 'en':
            if message == "현재 초상화와 새 초상화를 모두 선택해주세요.":
                message = "Please select both current and new portraits."
            elif message == "선택된 이미지 파일을 찾을 수 없습니다.":
                message = "Selected image file not found."
            elif message == "현재 초상화 폴더에 .bmp 형식의 이미지가 없습니다.":
                message = "No .bmp images found in the current portrait folder."
            elif message == "새 초상화 폴더에 .bmp 형식의 이미지가 없습니다.":
                message = "No .bmp images found in the new portrait folder."
            elif message == "현재 초상화 폴더에 624x804 이하 크기의 .bmp 이미지가 없습니다.":
                message = "No .bmp images under 624x804 size found in the current portrait folder."
            elif message == "새 초상화 폴더에 624x804 이하 크기의 .bmp 이미지가 없습니다.":
                message = "No .bmp images under 624x804 size found in the new portrait folder."
            elif "썸네일을 불러오는 중 오류가 발생했습니다" in message:
                message = message.replace("썸네일을 불러오는 중 오류가 발생했습니다", "Error occurred while loading thumbnails")
            elif "초상화 교체 중 오류가 발생했습니다" in message:
                message = message.replace("초상화 교체 중 오류가 발생했습니다", "Error occurred while replacing portrait")

        dialog = QDialog(self)
        dialog.setWindowTitle("Warning" if self.current_language == 'en' else "경고")
        layout = QVBoxLayout(dialog)
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)  # 중앙 정렬
        layout.addWidget(label)
        ok_button = QPushButton("OK" if self.current_language == 'en' else "확인")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def show_info(self, message):
        if self.current_language == 'en':
            if message == "초상화가 교체되었습니다.\n이전 초상화는 backup 폴더에 저장되었습니다.":
                message = "Portrait has been replaced.\nPrevious portrait has been saved in the backup folder."

        dialog = QDialog(self)
        dialog.setWindowTitle("Notice" if self.current_language == 'en' else "알림")
        layout = QVBoxLayout(dialog)
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)  # 중앙 정렬
        layout.addWidget(label)
        ok_button = QPushButton("OK" if self.current_language == 'en' else "확인")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        dialog.setLayout(layout)
        dialog.exec_()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "아이콘.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    window = PhotoManager()
    window.show()
    sys.exit(app.exec_())
