from pydantic import BaseModel
from fastapi import Form

class LoginForm(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        password: str = Form(...)
    ):
        return cls(email=email, password=password)

    @classmethod
    def get_examples(self):
        return {
            "test": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "email": "test@test.com",
                    "password": "test1234"
                },
            },
            "caca": {
                "summary": "An example with converted caca data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "email": "caca@caca.com",
                    "password": "caca"
                },
            }}



