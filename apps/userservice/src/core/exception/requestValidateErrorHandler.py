from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
def request_validate_exception_handler(request:Request, exception:RequestValidationError):
    # 提取所有错误详情
    errors = []
    for error in exception.errors():
        # loc 是一个列表，例如 ['query', 'page'] 或 ['body', 'user_id']
        # 取最后一个元素作为参数名（因为前面的通常是来源类型，如 'query'）
        field = error["loc"][-1]
        msg = error.get("msg", "参数校验失败")
        # 如果错误信息里包含具体的输入值，也一并带上
        input_value = error.get("input", None)
        
        errors.append({
            "field": field,           # 参数名
            "message": msg,           # 错误描述
            "input": input_value      # 用户实际传入的值（如果有）
        })
    
    # 拼接成一条简明错误消息（方便前端直接弹窗提示）
    error_messages = ", ".join([f"{e['field']}: {e['message']}" for e in errors])
    
    return JSONResponse(
        status_code=422,
        content={
            "code": 4000,
            "message": f"参数校验失败: {error_messages}",
            "errors": errors  # 保留完整的错误列表，方便前端逐个字段展示
        }
    )