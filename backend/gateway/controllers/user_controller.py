from fastapi.responses import JSONResponse


async def get_current_user(user: dict):
    try:
        return JSONResponse(status_code=200, content=user)
    except Exception as err:
        return JSONResponse(
            status_code=500, content={"message": f"getCurrentUser error: {err}"}
        )
