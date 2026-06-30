from app.database import SessionLocal
from sqlalchemy import inspect
from app.models.models import Producto
import sys


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else ""

    if action == "has_tables":
        db = SessionLocal()
        inspector = inspect(db.bind)
        has_productos = "productos" in inspector.get_table_names()
        db.close()
        print("t" if has_productos else "f")

    elif action == "product_count":
        db = SessionLocal()
        count = db.query(Producto).count()
        db.close()
        print(count)

    else:
        print(f"Acción desconocida: {action}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
