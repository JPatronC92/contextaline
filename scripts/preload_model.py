import sys
import os

def main():
    try:
        print("Descargando modelo all-MiniLM-L6-v2...")
        from sentence_transformers import SentenceTransformer
        
        # Pre-carga para que PyInstaller lo incluya en el caché
        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Modelo descargado. Realizando warm-up...")
        _ = model.encode(["warm up"], show_progress_bar=False)
        print("✓ Modelo listo")
        return 0
    except KeyboardInterrupt:
        print("\n⚠ Precarga interrumpida. El modelo se descargará en el primer uso.")
        return 0  # No es crítico, continuamos
    except Exception as e:
        print(f"⚠ Error en precarga: {e}")
        print("El modelo se descargará en el primer uso de la aplicación.")
        return 0  # No es crítico, continuamos

if __name__ == "__main__":
    sys.exit(main())
