from typing import List
from sqlalchemy.orm import Session
from kit.orm.database import SessionLocal
from kit.orm.model import Measure as DbMeasure
from shopping_list.domain.model import Measure
from shopping_list.domain.repository import MeasureRepository


class MeasureRepositoryImpl(MeasureRepository):
    def create(self, measure: Measure) -> Measure:
        db: Session = SessionLocal()
        db_measure = DbMeasure(name=measure.name)
        db.add(db_measure)
        db.commit()
        db.refresh(db_measure)
        return db_measure.to_domain_measure()

    def delete(self, measure_id: int) -> None:
        db: Session = SessionLocal()
        db_measure = db.query(DbMeasure).get(measure_id)
        db.delete(db_measure)
        db.commit()
        return

    def update(self, measure: Measure) -> Measure:
        db: Session = SessionLocal()
        db_measure: DbMeasure = db.query(DbMeasure).get(measure.id)
        db_measure.name = measure.name
        db.commit()
        db.refresh(db_measure)
        return db_measure.to_domain_measure()

    def find(self, measure_id: int) -> Measure:
        db: Session = SessionLocal()
        db_measure: DbMeasure = db.query(DbMeasure).get(measure_id)
        return db_measure.to_domain_measure()

    def find_all(self) -> List[Measure]:
        result: List[Measure] = []
        db: Session = SessionLocal()
        measures_db = db.query(DbMeasure).offset(0).all()
        for measure_db in measures_db:
            result.append(measure_db.to_domain_measure())
        return result
