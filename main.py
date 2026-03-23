from contextlib import asynccontextmanager
from typing import AsyncIterator

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel  # noqa: E402

from auth import anonymize_uid, create_firebase_custom_token, exchange_code_for_sub  # noqa: E402
from firebase_config import initialize_firebase  # noqa: E402


class TokenRequest(BaseModel):
    code: str


class TokenResponse(BaseModel):
    custom_token: str
    uid: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    initialize_firebase()
    yield


app = FastAPI(title="Google SSO Custom Auth", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/api/auth/custom-token", response_model=TokenResponse)
async def get_custom_token(req: TokenRequest) -> TokenResponse:
    try:
        google_sub = exchange_code_for_sub(req.code)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization code")

    uid = anonymize_uid(google_sub)

    try:
        custom_token = create_firebase_custom_token(uid)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to create custom token"
        )

    return TokenResponse(custom_token=custom_token, uid=uid)
