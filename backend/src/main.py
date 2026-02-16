from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Haetaan kirjautuneen käyttäjän tiedot ja kirjautumisen tila
from routes.users import router as user_router, current_user_id, logged_in
from ai_model import rag_cloud
from ai_model import utils
from bson import ObjectId
from database.db import users_collection
from routes.professional import router as professional_router


app = FastAPI()

# Alustetaan globaalien muuttujien tila
app.state.logged_in = False
app.state.current_user_id = None
app.state.current_user_data = None


# CORS (Allow frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.post("/api/send")
async def send_message(payload: dict):
    """
    1) Lukee frontendiltä tulevan 'message' ja (optionaalisen) 'user_id' -kentän.
    2) Jos user_id on annettu ja kelvollinen, hakee käyttäjädatan MongoDB:stä.
    3) Yhdistää käyttäjädatan promtiin ja kutsuu RAG-mallia.
    """
    
    logged_in = app.state.logged_in 

    # Muutettu käyttämään payloadia, requestin sijaan
    user_message = payload.get("message")
    user_id = app.state.current_user_id

    # jos haluaa muuttaa niin voi hakea user_datan suoraan globaalista muuttujasta ja käyttää sitä
    # nyt data haetaan ensin MongoDB:stä ja sitten asetetaan globaaliksi muuttujaksi
    # ja uudelleen sama tässä mainissa

    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required.")

    # 1) Haetaan käyttäjädata, jos user_id on annettu
    user_data = None
    if user_id:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user_id format.")
        user_doc = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"])  # Muunnetaan _id stringiksi
            user_data = user_doc

    # 2) Rakennetaan prompt, jossa lisätään käyttäjädata mukaan
    if logged_in and user_data and user_data.get("patient_info"):
        patient_info = user_data["patient_info"]
        prompt = f"{user_message}\n\nPatient info:\n{patient_info}"
    else:
        prompt = user_message

    # 3) Kutsutaan RAG-mallia
    try:
        raw_response = await rag_cloud.get_rag_response(prompt)
        formatted_text = utils.formatGeminiResponse(raw_response)
        return {"reply": formatted_text}
    except Exception as e:
        import traceback
        traceback.print_exc()  # Näyttää tarkemman syyn konsolissa
        raise HTTPException(status_code=500, detail=str(e))

# Register user routes
app.include_router(
    user_router,
    prefix="/users",
    tags=["users"]
    )

app.include_router(
    professional_router,
    prefix="/professional",
    tags=["professional"]
)