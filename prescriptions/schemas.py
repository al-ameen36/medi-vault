from pydantic import BaseModel
from users.schemas import UserType


class Drug(BaseModel):
    name: str
    dosage: str
    frequency: str


class PrescriptionBase(BaseModel):
    condition: str
    prescription: list[Drug]
    status: str


class PrescriptionCreateType(PrescriptionBase):
    patient: int


class PrescriptionType(PrescriptionBase):
    id: int
    patient: UserType
    doctor: UserType
