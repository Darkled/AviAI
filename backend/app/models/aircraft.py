from sqlalchemy import ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AircraftModel(Base):
    __tablename__ = "aircraft_models"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    manufacturer: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    range_km: Mapped[int] = mapped_column(Integer, nullable=False)
    cruise_speed_knots: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    fuel_burn_kg_per_hour: Mapped[float] = mapped_column(Float, nullable=False)

    fleet_items: Mapped[list["Fleet"]] = relationship(back_populates="aircraft_model")


class Fleet(Base):
    __tablename__ = "fleet"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tail_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("aircraft_models.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    aircraft_model: Mapped["AircraftModel"] = relationship(back_populates="fleet_items")
