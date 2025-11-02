import sys
import os
from pathlib import Path
import platform
import json
from time import time
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
                              QWidget, QInputDialog, QMessageBox, QFileDialog, QLabel, 
                              QLineEdit, QTextEdit, QListWidget, QProgressBar, QListWidgetItem,
                              QStyle, QComboBox, QMenu, QToolTip)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings, QTimer, QPoint
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QShortcut, QColor, QFont
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import List, Tuple, Optional
import docx
from pypdf import PdfReader

# Importaciones que funcionan tanto en desarrollo como en PyInstaller
try:
    from src.license import validate_license, save_license, load_license
    from src.app_version import APP_NAME, APP_VERSION
except ImportError:
    from license import validate_license, save_license, load_license
    from app_version import APP_NAME, APP_VERSION


class TfidfEmbedder:
    """Fallback simple basado en TF‑IDF para evitar dependencias nativas.
    Provee una interfaz .encode(list[str]) similar a SentenceTransformer.
    Se ajusta sobre el corpus en la primera llamada por búsqueda.
    """
    uses_corpus_fit = True

    def __init__(self, max_features: int = 4096):
        self.max_features = max_features
        self.vectorizer = TfidfVectorizer(max_features=max_features)
        self._fitted = False

    def start_new_corpus(self):
        """Resetea el estado para una nueva búsqueda/carpeta."""
        self.vectorizer = TfidfVectorizer(max_features=self.max_features)
        self._fitted = False

    def encode(self, texts: List[str], show_progress_bar: bool = False) -> np.ndarray:
        if not self._fitted:
            mat = self.vectorizer.fit_transform(texts)
            self._fitted = True
        else:
            mat = self.vectorizer.transform(texts)
        return mat.toarray().astype(np.float32)

def license_path():
    if platform.system() == "Windows":
        base = Path(os.getenv("APPDATA", Path.home()))
        lp = base / "JulioDevs" / "IDF" / "license.key"
    else:
        lp = Path.home() / ".config" / "idf" / "license.key"
    lp.parent.mkdir(parents=True, exist_ok=True)
    return lp

def ensure_license(parent_widget=None):
    lp = license_path()
    key = load_license(lp)
    hint = platform.node()  # o serial de disco si quieres algo más fuerte
    if key and validate_license(key, device_hint=hint):
        return True
    # Solicitar al usuario (QInputDialog o tu propio diálogo)
    key, ok = QInputDialog.getText(parent_widget, "Licencia", "Ingresa tu licencia JDL-XXXX-XXXX-XXXX:")
    if not ok:
        return False
    if validate_license(key, device_hint=hint):
        save_license(key, lp)
        return True
    QMessageBox.warning(parent_widget, "Licencia inválida", "La clave no es válida.")
    return False

class SearchWorker(QThread):
    """Worker thread para búsqueda de documentos"""
    progress = pyqtSignal(int)
    status_update = pyqtSignal(str)  # Nuevo: para actualizaciones de estado
    finished = pyqtSignal(list)
    
    def __init__(self, folder: str, query: str, model):
        super().__init__()
        self.folder = folder
        self.query = query
        self.model = model
        self._is_cancelled = False  # Control de cancelación
    
    def cancel(self):
        """Cancela la búsqueda en curso"""
        self._is_cancelled = True
        
    def run(self):
        results = self.search_documents(self.folder, self.query)
        self.finished.emit(results)

    # ---------------- Embedding cache helpers ---------------- #
    def _cache_dir(self) -> Path:
        if platform.system() == "Windows":
            base = Path(os.getenv("APPDATA", str(Path.home())))
            return base / "JulioDevs" / "IDF"
        else:
            return Path.home() / ".cache" / "idf"

    def _cache_path(self) -> Path:
        d = self._cache_dir()
        d.mkdir(parents=True, exist_ok=True)
        return d / "embedding_cache.json"

    def _load_cache(self) -> dict:
        p = self._cache_path()
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def _save_cache(self, data: dict):
        p = self._cache_path()
        try:
            tmp = p.with_suffix(".tmp")
            tmp.write_text(json.dumps(data), encoding="utf-8")
            tmp.replace(p)
        except Exception:
            pass

    def _file_fingerprint(self, fp: Path) -> Tuple[int, int]:
        try:
            s = fp.stat()
            return int(s.st_mtime), int(s.st_size)
        except Exception:
            return 0, 0
    
    def extract_text(self, file_path: Path) -> str:
        """Extrae texto de PDF, DOCX o TXT"""
        try:
            if file_path.suffix.lower() == '.pdf':
                reader = PdfReader(str(file_path))
                return ' '.join([page.extract_text() for page in reader.pages])
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                doc = docx.Document(str(file_path))
                return ' '.join([para.text for para in doc.paragraphs])
            elif file_path.suffix.lower() == '.txt':
                return file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
        return ""
    
    def search_documents(self, folder: str, query: str) -> List[Tuple[str, float]]:
        """Busca documentos similares usando embeddings con caché para acelerar."""
        folder_path = Path(folder)
        documents: List[Tuple[str, str]] = []

        # Buscar archivos
        self.status_update.emit("Buscando archivos...")
        extensions = ['.pdf', '.docx', '.doc', '.txt']
        files = [f for ext in extensions for f in folder_path.rglob(f'*{ext}')]

        if self._is_cancelled:
            return []

        total = max(1, len(files))
        self.status_update.emit(f"Procesando {total} archivos...")
        
        for idx, file_path in enumerate(files):
            if self._is_cancelled:
                return []
            
            self.status_update.emit(f"Extrayendo texto de {file_path.name}...")
            text = self.extract_text(file_path)
            if text:
                documents.append((str(file_path), text[:5000]))  # Limitar a 5000 chars
            self.progress.emit(int((idx + 1) / total * 60))  # 60% extracción

        if not documents:
            self.status_update.emit("No se encontraron documentos")
            return []

        # Si el modelo requiere ajustar sobre el corpus (fallback TF-IDF),
        # no usamos caché y calculamos todo on-the-fly.
        if getattr(self.model, "uses_corpus_fit", False):
            if self._is_cancelled:
                return []
            
            self.status_update.emit("Analizando documentos con IA...")
            # Asegurar que el vectorizador se ajusta al corpus actual
            getattr(self.model, "start_new_corpus", lambda: None)()
            corpus = [txt for (_p, txt) in documents]
            # Ajusta sobre documentos y devuelve matriz de documentos
            doc_embeddings = self.model.encode(corpus, show_progress_bar=False)
            # Embedding de la consulta con el mismo vectorizador
            query_embedding = self.model.encode([query], show_progress_bar=False)
            self.progress.emit(80)
        else:
            if self._is_cancelled:
                return []
            
            # Cargar/actualizar caché de embeddings (para SentenceTransformer)
            self.status_update.emit("Cargando caché de embeddings...")
            cache = self._load_cache()
            meta_key = "meta"
            entries = cache.get("entries", {})
            cache.setdefault("entries", entries)

            # Determinar qué documentos faltan en caché o están desactualizados
            need_indices = []
            for i, (path_str, _txt) in enumerate(documents):
                fp = Path(path_str)
                mtime, size = self._file_fingerprint(fp)
                rec = entries.get(path_str)
                if not rec or rec.get("mtime") != mtime or rec.get("size") != size:
                    need_indices.append(i)

            # Codificar en batch los faltantes
            if need_indices:
                self.status_update.emit(f"Generando embeddings para {len(need_indices)} documentos nuevos...")
                batch_texts = [documents[i][1] for i in need_indices]
                new_embs = self.model.encode(batch_texts, show_progress_bar=False)
                for idx_local, i in enumerate(need_indices):
                    if self._is_cancelled:
                        return []
                    path_str, _ = documents[i]
                    fp = Path(path_str)
                    mtime, size = self._file_fingerprint(fp)
                    vec = new_embs[idx_local].tolist()
                    entries[path_str] = {"mtime": mtime, "size": size, "vec": vec}
            self.progress.emit(80)  # 80% tras cache/encoding

            # Armar embeddings en el orden de documents
            doc_embeddings = np.array([entries[d[0]]["vec"] for d in documents], dtype=np.float32)

            # Guardar caché (best-effort)
            cache[meta_key] = {"updated_at": int(time())}
            self._save_cache(cache)

            # Generar embedding de la consulta
            self.status_update.emit("Analizando consulta...")
            query_embedding = self.model.encode([query], show_progress_bar=False)
        
        if self._is_cancelled:
            return []
        
        # Calcular similitudes
        self.status_update.emit("Calculando relevancia...")
        similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
        
        # Ordenar resultados
        self.status_update.emit("Ordenando resultados...")
        results = [(documents[i][0], float(similarities[i])) 
                   for i in range(len(documents))]
        results.sort(key=lambda x: x[1], reverse=True)
        
        self.progress.emit(100)
        self.status_update.emit("Búsqueda completada")
        return results[:20]  # Top 20 resultados

class DocumentFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, 1000, 700)
        
        # Configuración persistente
        self.settings = QSettings("JulioDevs", "IntelligentDocumentFinder")
        
        # Cargar geometría guardada
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        if not ensure_license(self):
            QMessageBox.critical(self, "Licencia", "Se requiere una licencia válida para continuar.")
            sys.exit(1)

        # Inicializar modelo
        self.model = None
        self.current_folder = None
        self.worker: Optional[SearchWorker] = None
        self.search_start_time = 0
        
        # Historial de búsquedas
        self.search_history = self.settings.value("search_history", [])
        if not isinstance(self.search_history, list):
            self.search_history = []
        
        self.init_ui()
        self.setup_shortcuts()
        self.apply_styles()
        self.load_model()
        
        # Cargar última carpeta usada
        last_folder = self.settings.value("last_folder")
        if last_folder and os.path.exists(last_folder):
            self.current_folder = last_folder
            self.folder_label.setText(f"📁 Carpeta: {last_folder}")
            self.search_btn.setEnabled(True)

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título con subtítulo
        title_container = QVBoxLayout()
        title_label = QLabel(f"<h1 style='margin:0;'>🔍 {APP_NAME}</h1>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label = QLabel("<p style='color:#666;'>Búsqueda inteligente de documentos con IA</p>")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_container.addWidget(title_label)
        title_container.addWidget(subtitle_label)
        layout.addLayout(title_container)
        
        # Selección de carpeta mejorada
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("📁 Carpeta: No seleccionada")
        self.folder_label.setStyleSheet("padding: 8px; background: #f0f0f0; border-radius: 4px;")
        self.select_folder_btn = QPushButton("📂 Seleccionar Carpeta")
        self.select_folder_btn.setToolTip("Ctrl+O - Abrir carpeta de documentos")
        self.select_folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_label, 1)
        folder_layout.addWidget(self.select_folder_btn)
        layout.addLayout(folder_layout)
        
        # Campo de búsqueda mejorado
        search_container = QVBoxLayout()
        search_layout = QHBoxLayout()
        
        # ComboBox editable para historial
        self.search_input = QComboBox()
        self.search_input.setEditable(True)
        self.search_input.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.search_input.lineEdit().setPlaceholderText("💡 Ej: contratos de arrendamiento del año 2024")
        self.search_input.addItems(self.search_history[:10])  # Últimas 10 búsquedas
        self.search_input.setCurrentText("")
        self.search_input.lineEdit().returnPressed.connect(self.start_search)
        
        self.search_btn = QPushButton("🔎 Buscar")
        self.search_btn.setToolTip("Enter o Ctrl+F - Iniciar búsqueda")
        self.search_btn.clicked.connect(self.start_search)
        self.search_btn.setEnabled(False)
        
        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.setToolTip("Escape - Cancelar búsqueda")
        self.cancel_btn.clicked.connect(self.cancel_search)
        self.cancel_btn.setVisible(False)
        
        self.clear_btn = QPushButton("🗑️ Limpiar")
        self.clear_btn.setToolTip("Ctrl+R - Limpiar resultados")
        self.clear_btn.clicked.connect(self.clear_results)
        
        search_layout.addWidget(QLabel("🔍 Buscar:"))
        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.cancel_btn)
        search_layout.addWidget(self.clear_btn)
        
        # Etiqueta de ayuda
        help_label = QLabel("💡 Tip: Describe lo que buscas en lenguaje natural. La IA entenderá el contexto.")
        help_label.setStyleSheet("color: #666; font-size: 11px; font-style: italic;")
        
        search_container.addLayout(search_layout)
        search_container.addWidget(help_label)
        layout.addLayout(search_container)
        
        # Barra de progreso con label de estado
        progress_container = QVBoxLayout()
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #0066cc; font-weight: bold;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_container.addWidget(self.status_label)
        progress_container.addWidget(self.progress_bar)
        layout.addLayout(progress_container)
        
        # Resultados con contador
        results_header = QHBoxLayout()
        self.results_label = QLabel("📊 Resultados:")
        self.results_count = QLabel("")
        results_header.addWidget(self.results_label)
        results_header.addWidget(self.results_count)
        results_header.addStretch()
        layout.addLayout(results_header)
        
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.open_document)
        self.results_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.results_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.results_list)
        
        # Botones inferiores
        bottom_layout = QHBoxLayout()
        self.cache_info_label = QLabel("")
        self.cache_info_label.setStyleSheet("color: #666; font-size: 10px;")
        
        self.about_button = QPushButton("ℹ️ Acerca de")
        self.about_button.clicked.connect(self.show_about_dialog)
        
        bottom_layout.addWidget(self.cache_info_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.about_button)
        layout.addLayout(bottom_layout)
    
    def setup_shortcuts(self):
        """Configura atajos de teclado"""
        # Ctrl+O: Abrir carpeta
        open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        open_shortcut.activated.connect(self.select_folder)
        
        # Ctrl+F: Enfocar búsqueda
        focus_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        focus_shortcut.activated.connect(lambda: self.search_input.setFocus())
        
        # Ctrl+R: Limpiar resultados
        clear_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        clear_shortcut.activated.connect(self.clear_results)
        
        # Escape: Cancelar búsqueda
        cancel_shortcut = QShortcut(QKeySequence("Escape"), self)
        cancel_shortcut.activated.connect(self.cancel_search)
        
        # F1: Ayuda
        help_shortcut = QShortcut(QKeySequence("F1"), self)
        help_shortcut.activated.connect(self.show_help)
    
    def apply_styles(self):
        """Aplica estilos CSS a la aplicación"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #0066cc;
                border-radius: 4px;
                background-color: #0066cc;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                border-color: #cccccc;
                color: #666666;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
                background-color: #ffffff;
                color: #000000;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #0066cc;
                background-color: #ffffff;
                color: #000000;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                selection-background-color: #e3f2fd;
                selection-color: #0066cc;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
                background-color: #ffffff;
                color: #000000;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
                color: #000000;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #0066cc;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
                height: 25px;
                color: #000000;
            }
            QProgressBar::chunk {
                background-color: #0066cc;
                border-radius: 3px;
            }
            QLabel {
                color: #000000;
            }
            QStatusBar {
                color: #000000;
            }
        """)

    def load_model(self):
        """Carga el modelo de ML"""
        try:
            self.statusBar().showMessage("⏳ Cargando modelo de IA...")
            # Importación diferida para evitar fallos de DLL al importar el módulo en arranque.
            from sentence_transformers import SentenceTransformer  # type: ignore
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.statusBar().showMessage("✅ Modelo cargado - Listo para buscar", 3000)
        except Exception as e:
            # Fallback sin PyTorch: TF-IDF sobre el corpus
            # Mantiene la app usable en entornos sin dependencias nativas.
            self.model = TfidfEmbedder()
            QMessageBox.information(self, "⚠️ Modo básico activado",
                                    "No se pudo cargar el modelo de IA avanzado.\n\n"
                                    "🔧 Se activó un modo básico de búsqueda (TF-IDF).\n"
                                    "La aplicación funcionará correctamente, pero con menor precisión.\n\n"
                                    f"💡 Detalle técnico: {str(e)[:100]}...")
            self.statusBar().showMessage("⚡ Modo básico (TF‑IDF) listo", 5000)
    
    def select_folder(self):
        """Selecciona la carpeta de documentos"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "📂 Seleccionar carpeta de documentos",
            self.current_folder or ""
        )
        if folder:
            self.current_folder = folder
            self.settings.setValue("last_folder", folder)
            self.folder_label.setText(f"📁 Carpeta: {folder}")
            self.search_btn.setEnabled(True)
            self.statusBar().showMessage(f"✅ Carpeta seleccionada: {folder}", 3000)
    
    def start_search(self):
        """Inicia la búsqueda"""
        query = self.search_input.currentText().strip()
        if not query:
            QMessageBox.warning(self, "⚠️ Campo vacío", 
                              "Por favor ingresa un término de búsqueda.\n\n"
                              "💡 Ejemplos:\n"
                              "• contratos de arrendamiento 2024\n"
                              "• facturas de servicios\n"
                              "• informes financieros")
            return
        
        if not self.current_folder:
            QMessageBox.warning(self, "⚠️ Carpeta no seleccionada", 
                              "Por favor selecciona una carpeta primero.\n\n"
                              "📂 Usa el botón 'Seleccionar Carpeta' o presiona Ctrl+O")
            return
        
        # Guardar en historial
        if query not in self.search_history:
            self.search_history.insert(0, query)
            self.search_history = self.search_history[:20]  # Mantener solo 20
            self.settings.setValue("search_history", self.search_history)
            self.search_input.insertItem(0, query)
        
        # Deshabilitar controles
        self.search_btn.setEnabled(False)
        self.search_btn.setVisible(False)
        self.cancel_btn.setVisible(True)
        self.select_folder_btn.setEnabled(False)
        self.search_input.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.results_list.clear()
        self.results_count.setText("")
        self.search_start_time = time()
        self.statusBar().showMessage("🔍 Buscando...")
        
        # Iniciar worker thread
        self.worker = SearchWorker(self.current_folder, query, self.model)
        self.worker.progress.connect(self.update_progress)
        self.worker.status_update.connect(self.update_status)
        self.worker.finished.connect(self.show_results)
        self.worker.start()
    
    def cancel_search(self):
        """Cancela la búsqueda en curso"""
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.statusBar().showMessage("❌ Cancelando búsqueda...", 2000)
    
    def clear_results(self):
        """Limpia los resultados de búsqueda"""
        self.results_list.clear()
        self.results_count.setText("")
        self.statusBar().showMessage("🗑️ Resultados limpiados", 2000)
    
    def update_progress(self, value):
        """Actualiza la barra de progreso"""
        self.progress_bar.setValue(value)
        elapsed = time() - self.search_start_time
        self.statusBar().showMessage(f"🔍 Buscando... ({elapsed:.1f}s)")
    
    def update_status(self, status: str):
        """Actualiza el label de estado"""
        self.status_label.setText(f"⚙️ {status}")
    
    def show_results(self, results):
        """Muestra los resultados de búsqueda"""
        elapsed = time() - self.search_start_time
        self.progress_bar.setVisible(False)
        self.status_label.setText("")
        self.search_btn.setEnabled(True)
        self.search_btn.setVisible(True)
        self.cancel_btn.setVisible(False)
        self.select_folder_btn.setEnabled(True)
        self.search_input.setEnabled(True)
        
        if not results:
            QMessageBox.information(self, "🔍 Sin resultados", 
                                   "No se encontraron documentos relevantes.\n\n"
                                   "💡 Sugerencias:\n"
                                   "• Intenta con términos más generales\n"
                                   "• Verifica que la carpeta contenga documentos\n"
                                   "• Revisa que los archivos sean PDF, DOCX o TXT")
            self.statusBar().showMessage(f"❌ Sin resultados ({elapsed:.1f}s)", 3000)
            return
        
        self.results_list.clear()
        for file_path, score in results:
            filename = Path(file_path).name
            file_obj = Path(file_path)
            
            # Obtener metadata
            try:
                stat = file_obj.stat()
                size_mb = stat.st_size / (1024 * 1024)
                mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M")
                
                # Determinar emoji por relevancia
                if score >= 0.8:
                    emoji = "🟢"
                elif score >= 0.6:
                    emoji = "🟡"
                else:
                    emoji = "🟠"
                
                # Crear item con formato mejorado
                item_text = (f"{emoji} {filename}\n"
                           f"    📊 Relevancia: {score:.2%} | "
                           f"📅 {mod_time} | "
                           f"📏 {size_mb:.2f} MB\n"
                           f"    📂 {file_path}")
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, file_path)
                
                # Color de fondo según relevancia
                if score >= 0.8:
                    item.setBackground(QColor(232, 245, 233))  # Verde claro
                elif score >= 0.6:
                    item.setBackground(QColor(255, 249, 196))  # Amarillo claro
                
                self.results_list.addItem(item)
            except Exception as e:
                # Fallback si hay error al obtener metadata
                item_text = f"📄 {filename} (Score: {score:.3f})\n    {file_path}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, file_path)
                self.results_list.addItem(item)
        
        self.results_count.setText(f"({len(results)} documentos encontrados)")
        self.statusBar().showMessage(f"✅ Búsqueda completada en {elapsed:.1f}s - {len(results)} documentos encontrados", 5000)
    
    def open_document(self, item):
        """Abre el documento seleccionado"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        
        if not file_path:
            # Fallback: extraer de texto
            text = item.text()
            lines = text.split('\n')
            for line in lines:
                if line.strip().startswith("📂"):
                    file_path = line.strip()[2:].strip()
                    break
        
        if file_path and os.path.exists(file_path):
            try:
                os.startfile(file_path)
                self.statusBar().showMessage(f"📂 Abriendo: {Path(file_path).name}", 3000)
            except Exception as e:
                QMessageBox.warning(self, "❌ Error al abrir", 
                                  f"No se pudo abrir el archivo.\n\n"
                                  f"Error: {str(e)}")
        else:
            QMessageBox.warning(self, "❌ Archivo no encontrado", 
                              "El archivo no existe o fue movido.")
    
    def show_context_menu(self, position: QPoint):
        """Muestra menú contextual en resultados"""
        item = self.results_list.itemAt(position)
        if not item:
            return
        
        file_path = item.data(Qt.ItemDataRole.UserRole)
        if not file_path:
            return
        
        menu = QMenu(self)
        
        open_action = menu.addAction("📂 Abrir documento")
        open_folder_action = menu.addAction("📁 Abrir ubicación")
        copy_path_action = menu.addAction("📋 Copiar ruta")
        menu.addSeparator()
        properties_action = menu.addAction("ℹ️ Propiedades")
        
        action = menu.exec(self.results_list.mapToGlobal(position))
        
        if action == open_action:
            self.open_document(item)
        elif action == open_folder_action:
            try:
                os.startfile(os.path.dirname(file_path))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo abrir la carpeta:\n{e}")
        elif action == copy_path_action:
            QApplication.clipboard().setText(file_path)
            self.statusBar().showMessage("📋 Ruta copiada al portapapeles", 2000)
        elif action == properties_action:
            self.show_file_properties(file_path)
    
    def show_file_properties(self, file_path: str):
        """Muestra propiedades del archivo"""
        try:
            file_obj = Path(file_path)
            stat = file_obj.stat()
            size_mb = stat.st_size / (1024 * 1024)
            created = datetime.fromtimestamp(stat.st_ctime).strftime("%d/%m/%Y %H:%M:%S")
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S")
            
            props = (f"📄 Nombre: {file_obj.name}\n\n"
                    f"📂 Ubicación: {file_obj.parent}\n\n"
                    f"📏 Tamaño: {size_mb:.2f} MB ({stat.st_size:,} bytes)\n\n"
                    f"📅 Creado: {created}\n\n"
                    f"📅 Modificado: {modified}\n\n"
                    f"📝 Tipo: {file_obj.suffix.upper()[1:]} Document")
            
            QMessageBox.information(self, "ℹ️ Propiedades del Archivo", props)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron obtener las propiedades:\n{e}")
    
    def show_help(self):
        """Muestra ayuda"""
        help_text = """
        <h2>🔍 Ayuda - IntelligentDocumentFinder</h2>
        
        <h3>⌨️ Atajos de Teclado:</h3>
        <ul>
            <li><b>Ctrl+O</b> - Seleccionar carpeta</li>
            <li><b>Ctrl+F</b> - Enfocar búsqueda</li>
            <li><b>Enter</b> - Iniciar búsqueda</li>
            <li><b>Ctrl+R</b> - Limpiar resultados</li>
            <li><b>Escape</b> - Cancelar búsqueda</li>
            <li><b>F1</b> - Mostrar esta ayuda</li>
        </ul>
        
        <h3>🎯 Cómo Buscar:</h3>
        <ul>
            <li>Describe lo que buscas en lenguaje natural</li>
            <li>La IA entenderá el contexto y significado</li>
            <li>No necesitas el nombre exacto del archivo</li>
        </ul>
        
        <h3>💡 Ejemplos:</h3>
        <ul>
            <li>"contratos de arrendamiento 2024"</li>
            <li>"facturas de servicios públicos"</li>
            <li>"informes financieros primer trimestre"</li>
        </ul>
        
        <h3>🖱️ En los Resultados:</h3>
        <ul>
            <li><b>Doble clic</b> - Abrir documento</li>
            <li><b>Clic derecho</b> - Menú contextual</li>
            <li>Colores indican relevancia: 🟢 Alta, 🟡 Media, 🟠 Baja</li>
        </ul>
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("❓ Ayuda")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(help_text)
        msg.exec()

    def show_about_dialog(self):
        about_text = f"""
        <h2>🔍 {APP_NAME}</h2>
        <p><b>Versión:</b> {APP_VERSION}</p>
        
        <p>Buscador inteligente de documentos usando Inteligencia Artificial</p>
        
        <p><b>Características:</b></p>
        <ul>
            <li>✨ Búsqueda semántica con IA</li>
            <li>📄 Soporta PDF, DOCX y TXT</li>
            <li>⚡ Sistema de caché rápido</li>
            <li>🎯 Resultados por relevancia</li>
        </ul>
        
        <p>© 2025 JulioDevs - Todos los derechos reservados</p>
        
        <p style='font-size: 10px; color: #666;'>
        Desarrollado con PyQt6 y Sentence Transformers
        </p>
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("ℹ️ Acerca de")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(about_text)
        msg.exec()
    
    def closeEvent(self, event):
        """Guarda configuración al cerrar"""
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = DocumentFinderApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
