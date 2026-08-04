from pydantic import BaseModel, field_validator, EmailStr, model_validator, ConfigDict
from pydantic_core import PydanticCustomError


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    pwd: str
    confirmPwd: str

    @field_validator("pwd")
    @classmethod
    def validate_pwd(cls, value):
        if len(value) < 5:
            raise PydanticCustomError("", "密码过于简单，请更换")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value) > 10:
            raise PydanticCustomError("", "昵称过长，请更换")
        return value

    @model_validator(mode="after")
    def check_pwd_macth(
        self,
    ):
        if self.pwd != self.confirmPwd:
            raise PydanticCustomError("", "两次输入的密码不一致")
        return self


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
