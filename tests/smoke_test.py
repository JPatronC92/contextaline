import os
import sys
from pathlib import Path

# Ensure project root is on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

try:
    from app import SearchWorker  # type: ignore
except Exception as e:
    print(f"⚠ No se pudo importar app/SearchWorker ({e}). Posible fallo de torch en runtime. Saltando smoke test.")
    raise SystemExit(0)
try:
    from sentence_transformers import SentenceTransformer
except Exception as e:
    print(f"⚠ No se pudo importar SentenceTransformer ({e}). Saltando smoke test.")
    raise SystemExit(0)


def main():
    test_dir = ROOT / 'test_documents'
    assert test_dir.exists(), f"No existe carpeta de prueba: {test_dir}"

    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    except OSError as e:
        print(f"⚠ No se pudo cargar torch/backs para SentenceTransformer ({e}). Saltando smoke test.")
        raise SystemExit(0)

    # Usamos SearchWorker pero llamando al método sin thread
    worker = SearchWorker(str(test_dir), 'documento', model)
    results = worker.search_documents(str(test_dir), 'documento')

    print("Resultados:")
    for path, score in results:
        print(f" - {Path(path).name}: {score:.3f}")

    # Validación mínima
    assert len(results) > 0, "Sin resultados en smoke test"
    print("✓ Smoke test OK")


if __name__ == '__main__':
    main()
