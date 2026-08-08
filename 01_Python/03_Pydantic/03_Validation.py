from pydantic import BaseModel, field_validator, model_validator

# field_validator

# class User(BaseModel):

#     age: int

#     @field_validator("age")
#     @classmethod
#     def check_age(cls, value):

#         if value < 18:
#             raise ValueError("Must be adult")

#         return value


# user = User(age=25)
# print(user)

# mode="before"

class User1(BaseModel):

    price: int

    @field_validator("price", mode="before")
    @classmethod
    def clean_age(cls, value):

        print(value)
        print(type(value))

        return value

user1 = User1(price="30")
print(user1)

# model_validator

class User(BaseModel):

    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self):

        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        return self