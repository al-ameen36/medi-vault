import os
from typing import Annotated
from fastapi import APIRouter, Depends
from supabase import Client
from db.controller import get_db
from prescriptions.controller import (
    add_prescription,
    delete_prescription,
    dispense_presc,
    get_all,
    get_prescription,
)
from prescriptions.schemas import PrescriptionCreateType
from users.controller import (
    get_current_user,
)
from users.schemas import UserType


SECRET = os.environ.get("SECRET")
router = APIRouter()


@router.get("")
async def read_prescriptions(
    current_user: Annotated[UserType, Depends(get_current_user)],
    db: Client = Depends(get_db),
):
    prescriptions = get_all(db, current_user.id)
    return {"detail": "Prescriptions fetched successfully", "data": prescriptions}


@router.get("/{prescription_id}")
def read_prescription(prescription_id: int, db: Client = Depends(get_db)):
    prescription = get_prescription(db, prescription_id)
    return {
        "detail": "Prescription fetched successfully",
        "data": prescription,
    }


@router.get("/{prescription_id}/dispense/{dispenser_id}")
def dispense_prescription(
    dispenser_id: int,
    prescription_id: int,
    db: Client = Depends(get_db),
):
    dispense_presc(db, prescription_id, dispenser_id)
    return {
        "detail": "Prescription dispensed successfully",
    }


@router.post("")
async def create_prescriptions(
    prescription: PrescriptionCreateType,
    current_user: Annotated[UserType, Depends(get_current_user)],
    db: Client = Depends(get_db),
):
    prescription = add_prescription(db, current_user.id, prescription)
    return {
        "detail": "Prescription added successfully",
        "data": prescription.model_dump(),
    }


@router.delete("/{prescription_id}")
def remove_prescription(prescription_id: int, db: Client = Depends(get_db)):
    prescription = delete_prescription(db, prescription_id)
    return {"detail": "Prescription deleted successfully"}
