from fastapi import APIRouter, Depends

router = APIRouter(tags=["Auth"])

@router.post("/signup")
async def signup():
    pass

@router.post("/login")
async def login():
    pass

@router.post("/logout")
async def logout():
    pass

@router.get("/me")
async def me():
    pass

@router.post("/send-email")
async def send_email():
    pass

@router.post("/verify-email")
async def verify_email():
    pass

@router.post("/reset-password")
async def reset_password():
    pass

@router.post("/reset-password")
async def reset_password():
    pass