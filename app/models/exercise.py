from sqlalchemy import String, Text, JSON, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id: Mapped[str] = mapped_column(String(50), primary_key = True)
    exercise_category: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(200))
    target_muscles: Mapped[list] = mapped_column(JSON)
    secondary_muscles: Mapped[list] = mapped_column(JSON)
    gym_required: Mapped[bool] = mapped_column(Boolean)
    equipments: Mapped[list] = mapped_column(JSON)

