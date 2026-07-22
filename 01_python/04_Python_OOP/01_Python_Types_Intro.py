def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))

def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))

from typing import Union, Optional


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")

def say_hi(name: Optional[str]):
    print(f"Hey {name}!")

def say_hi(name: str | None):
    print(f"Hey {name}!")


say_hi("Rahim")      # Output: Hi Rahim!
say_hi(name=None)    # Output: Hi None!

def say_hi(name: str | None):
    if name is not None:
        print(f"Hello {name}!")
    else:
        print("Hello World!")