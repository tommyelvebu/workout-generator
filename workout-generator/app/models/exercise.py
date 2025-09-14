from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id: Mapped[str] = mapped_column(String(50), primary_key = True)
    name: Mapped[str] = mapped_column(String(200))
    gif_url: Mapped[str] = mapped_column(Text)
    target_muscles: Mapped[list] = mapped_column(JSON)
    secondary_muscles: Mapped[list] = mapped_column(JSON)
    body_parts: Mapped[list] = mapped_column(JSON)
    equipments: Mapped[list] = mapped_column(JSON)
    instructions: Mapped[list] = mapped_column(JSON)