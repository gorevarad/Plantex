from fastapi import FastAPI
from routes.predict import router as predict_router

app = FastAPI()

# Include the routes
app.include_router(predict_router)

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
