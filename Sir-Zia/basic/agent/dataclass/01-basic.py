from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    price: float

# Ab ek object create karte hain
my_book = Book("Atomic Habits", "James Clear", 1500.0)

print('\n The Result is:')
print(my_book)
