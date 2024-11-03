from fastapi import HTTPException
from supabase import Client
from prescriptions.schemas import PrescriptionCreateType, PrescriptionType


def get_all(db: Client, doctor_id: int):
    prescription = (
        db.table("prescriptions").select("*").eq("doctor", doctor_id).execute()
    )

    print(prescription)
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription.data


def get_prescription(db: Client, prescription_id: int):
    prescription = (
        db.table("prescriptions").select("*").eq("id", prescription_id).execute()
    )

    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription


def add_prescription(db: Client, user_id: int, prescription: PrescriptionCreateType):
    try:
        db_prescription = (
            db.table("prescriptions")
            .insert({**prescription.model_dump(), "doctor": user_id})
            .execute()
        )
        return PrescriptionCreateType(**db_prescription.data[0])
    except Exception as error:
        print(error)
        raise HTTPException(status_code=400, detail="Could not create prescription")


def delete_prescription(db: Client, prescription_id: int):
    try:
        db.table("prescriptions").delete().eq("id", prescription_id).execute()
        return True
    except Exception as error:
        print(error)
        raise HTTPException(status_code=400, detail="Could not create prescription")


def dispense_prescription(db: Client, prescription_id: int):
    prescription = {}
    return True