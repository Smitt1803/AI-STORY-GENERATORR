from pydantic import BaseModel, EmailStr

# User Registration Schema
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

# User Login Schema (Uses Email & Password)
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str