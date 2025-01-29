from fastapi import FastAPI
from routers import auth, booking

app = FastAPI(title = "Barbershop API")


app.include_router(auth.router, prefix = "/auth", tags = ['Auth'])
app.include_router(booking.router, prefix = "/booking", tags = ["Booking"])

@app.get("/")
async def root():
    return {"message": "Barbershop API is running!"}