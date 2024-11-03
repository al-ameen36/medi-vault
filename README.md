
# PrescribeMe
This app integrates TNID for identity verification, enabling a trusted prescription process from diagnosis to dispensation.

## How It Works
1.  **User Registration**: Users sign up in the app and are verified through their existing TNID profile, ensuring identity and information reliability.
    
2.  **Consultation**: After logging in, users can consult with licensed doctors via secure video chat within the app. Doctors assess symptoms, discuss health concerns, and make diagnoses in real-time.
    
3.  **Prescription Issuance**: If medication is required, the doctor generates a digital prescription through the app. This prescription includes necessary information about the medicine and dosage.
    
4.  **Pharmacy Visit with QR Code**: Users receive a unique QR code in the app for their prescription. At the pharmacy, they can present this QR code, which the pharmacist scans to access the verified prescription details.
    
5.  **Medication Dispensation**: The pharmacist confirms the legitimacy of the prescription through the app, then dispenses the medication according to the doctor’s instructions.
    
## Tools used
1. TNID
2. Supabase
3. FastAPI

## How to setup
1. Run `mkdir .ssh`
2. Create private key  `openssl genpkey -algorithm RSA -out .ssh/private_key.pem -pkeyopt rsa_keygen_bits:2048`
3. Create public key `openssl rsa -pubout -in .ssh/private_key.pem -out .ssh/public_key.pem
`
4. Create a .env file and add a `OPENAI_API_KEY=` variable (get your API key from [OpenAI](https://platform.openai.com/organization/api-keys)).
6. Create the `.env` file from `.env.example` file and fill in all variables
7. Run `python -m venv venv`
8. On Window run `./venv/Scripts/activate`
9. On Mac/Linux run `source venv/bin/activate`
10. Run `pip install -r requirements.txt` in the terminal.
11. Run `fastapi run main.py`
