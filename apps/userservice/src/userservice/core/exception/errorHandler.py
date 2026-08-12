from fastapi.responses import JSONResponse
from fastapi import Request


async def exception_handler(request: Request, exception: Exception):
    # return JSONResponse(
    #     status_code=500,
    #     content={
    #         "code": 4000,
    #         "message": f"{str(exception)}",
    #     },
    # )
    print("exception_handler+++++++++")
    try:
        print("handled+++++++++")

        return JSONResponse(
            status_code=500,
            content={
                "code": 4000,
                # "message": f"{str(exception)}",
                "message": "1233",
            },
        )
    except Exception as e:
        # 记录处理器自身的异常
        print(f"Exception handler failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"code": 5000, "message": "Internal error in handler"},
        )
