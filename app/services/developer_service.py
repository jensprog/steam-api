from sqlalchemy.orm import Session
from app.models.developer import Developer
from app.schemas import DeveloperResponse
from app.utils.serializers import serialize_developer


def get_developers_list(db: Session) -> list[DeveloperResponse]:
    developers = db.query(Developer).all()
    return [serialize_developer(dev) for dev in developers]
