from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Body
from app.api import deps
from app.models.user import User
from app.services.payment_service import payment_service

router = APIRouter()

@router.post("/verify")
async def verify_payment(
    imp_uid: str = Body(...),
    merchant_uid: str = Body(...),
    amount: int = Body(...),
    tier: str = Body(...),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Verify payment result from frontend and upgrade user tier.
    """
    is_valid = await payment_service.verify_payment(imp_uid, merchant_uid, amount)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Payment verification failed")
    
    # Upgrade user
    await payment_service.upgrade_user_tier(current_user.email, tier)
    
    return {"status": "success", "message": f"Upgraded to {tier}"}
