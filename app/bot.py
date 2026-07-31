from app.database import Base, engine
from app.models import Deal


def main():
    print("=" * 50)
    print(" Deal Platform")
    print("=" * 50)

    print("Veritabanı tabloları oluşturuluyor...")
    Base.metadata.create_all(bind=engine)

    print("✓ Sistem başarıyla başlatıldı.")


if __name__ == "__main__":
    main()
