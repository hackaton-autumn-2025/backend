from .history_controller import router as history_router
from .user_controller import router as user_router
from .work_location_controller import router as loc_router

__all__ = ["history_router", "loc_router", "user_router"]
