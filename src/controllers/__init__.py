from .user_controller import router as user_router
from .work_location_controller import router as loc_router
from .history_controller import router as history_router

__all__ = ["loc_router", "user_router", "history_router"]
