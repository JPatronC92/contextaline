import sys
import os
from pathlib import Path
import platform
import json
from time import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
                              QWidget, QInputDialog, QMessageBox, QFileDialog, QLabel, 
                              QLineEdit, QTextEdit, QListWidget, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import List, Tuple
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
    finished = pyqtSignal(list)
    
    def __init__(self, folder: str, query: str, model):
        super().__init__()
        self.folder = folder
        self.query = query
        self.model = model
        
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
        extensions = ['.pdf', '.docx', '.doc', '.txt']
        files = [f for ext in extensions for f in folder_path.rglob(f'*{ext}')]

        total = max(1, len(files))
        for idx, file_path in enumerate(files):
            text = self.extract_text(file_path)
            if text:
                documents.append((str(file_path), text[:5000]))  # Limitar a 5000 chars
            self.progress.emit(int((idx + 1) / total * 60))  # 60% extracción

        if not documents:
            return []

        # Si el modelo requiere ajustar sobre el corpus (fallback TF-IDF),
        # no usamos caché y calculamos todo on-the-fly.
        if getattr(self.model, "uses_corpus_fit", False):
            # Asegurar que el vectorizador se ajusta al corpus actual
            getattr(self.model, "start_new_corpus", lambda: None)()
            corpus = [txt for (_p, txt) in documents]
            # Ajusta sobre documentos y devuelve matriz de documentos
            doc_embeddings = self.model.encode(corpus, show_progress_bar=False)
            # Embedding de la consulta con el mismo vectorizador
            query_embedding = self.model.encode([query], show_progress_bar=False)
            self.progress.emit(80)
        else:
            # Cargar/actualizar caché de embeddings (para SentenceTransformer)
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
                batch_texts = [documents[i][1] for i in need_indices]
                new_embs = self.model.encode(batch_texts, show_progress_bar=False)
                for idx_local, i in enumerate(need_indices):
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
            query_embedding = self.model.encode([query], show_progress_bar=False)
        
        # Calcular similitudes
        similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
        
    # Ordenar resultados
        results = [(documents[i][0], float(similarities[i])) 
                   for i in range(len(documents))]
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:20]  # Top 20 resultados

class DocumentFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, 900, 600)

        if not ensure_license(self):
            QMessageBox.critical(self, "Licencia", "Se requiere una licencia válida para continuar.")
            sys.exit(1)

        # Inicializar modelo
        self.model = None
        self.current_folder = None
        
        self.init_ui()
        self.load_model()

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        
        # Título
        title_label = QLabel(f"<h2>{APP_NAME}</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Selección de carpeta
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Carpeta: No seleccionada")
        self.select_folder_btn = QPushButton("Seleccionar Carpeta")
        self.select_folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.select_folder_btn)
        layout.addLayout(folder_layout)
        
        # Campo de búsqueda
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ej: contratos de arrendamiento del año 2024")
        self.search_btn = QPushButton("Buscar")
        self.search_btn.clicked.connect(self.start_search)
        self.search_btn.setEnabled(False)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Resultados
        results_label = QLabel("Resultados:")
        layout.addWidget(results_label)
        
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.open_document)
        layout.addWidget(self.results_list)
        
        # Botones inferiores
        bottom_layout = QHBoxLayout()
        self.about_button = QPushButton("Acerca de")
        self.about_button.clicked.connect(self.show_about_dialog)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.about_button)
        layout.addLayout(bottom_layout)

    def load_model(self):
        """Carga el modelo de ML"""
        try:
            self.statusBar().showMessage("Cargando modelo de IA...")
            # Importación diferida para evitar fallos de DLL al importar el módulo en arranque.
            from sentence_transformers import SentenceTransformer  # type: ignore
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.statusBar().showMessage("Modelo cargado - Listo para buscar", 3000)
        except Exception as e:
            # Fallback sin PyTorch: TF-IDF sobre el corpus
            # Mantiene la app usable en entornos sin dependencias nativas.
            self.model = TfidfEmbedder()
            QMessageBox.information(self, "Modo básico activado",
                                    "No se pudo cargar el backend de IA acelerado (PyTorch).\n"
                                    "Se activó un modo básico de búsqueda (TF‑IDF).\n"
                                    f"Detalle: {e}")
            self.statusBar().showMessage("Modo básico (TF‑IDF) listo", 5000)
    
    def select_folder(self):
        """Selecciona la carpeta de documentos"""
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de documentos")
        if folder:
            self.current_folder = folder
            self.folder_label.setText(f"Carpeta: {folder}")
            self.search_btn.setEnabled(True)
            self.statusBar().showMessage(f"Carpeta seleccionada: {folder}", 3000)
    
    def start_search(self):
        """Inicia la búsqueda"""
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Advertencia", "Por favor ingresa un término de búsqueda")
            return
        
        if not self.current_folder:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona una carpeta primero")
            return
        
        # Deshabilitar controles
        self.search_btn.setEnabled(False)
        self.select_folder_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.results_list.clear()
        self.statusBar().showMessage("Buscando...")
        
        # Iniciar worker thread
        self.worker = SearchWorker(self.current_folder, query, self.model)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.show_results)
        self.worker.start()
    
    def update_progress(self, value):
        """Actualiza la barra de progreso"""
        self.progress_bar.setValue(value)
    
    def show_results(self, results):
        """Muestra los resultados de búsqueda"""
        self.progress_bar.setVisible(False)
        self.search_btn.setEnabled(True)
        self.select_folder_btn.setEnabled(True)
        
        if not results:
            QMessageBox.information(self, "Sin resultados", 
                                   "No se encontraron documentos relevantes")
            self.statusBar().showMessage("Sin resultados", 3000)
            return
        
        self.results_list.clear()
        for file_path, score in results:
            filename = Path(file_path).name
            self.results_list.addItem(f"{filename} (Score: {score:.3f}) - {file_path}")
        
        self.statusBar().showMessage(f"Se encontraron {len(results)} documentos", 5000)
    
    def open_document(self, item):
        """Abre el documento seleccionado"""
        text = item.text()
        # Extraer ruta del texto
        path_start = text.rfind(" - ") + 3
        file_path = text[path_start:]
        
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            QMessageBox.warning(self, "Error", "El archivo no existe")

    def show_about_dialog(self):
        QMessageBox.about(self, "Acerca de", 
                         f"{APP_NAME}\nVersión: {APP_VERSION}\n\n"
                         f"Buscador inteligente de documentos usando IA\n"
                         f"© 2025 JulioDevs")

def main():
    app = QApplication(sys.argv)
    window = DocumentFinderApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
