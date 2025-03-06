import numpy as np
from dataclasses import dataclass



# A class defines a "class" of objects.
# Each class has a set of attributes (variables), and methods (functions)
# examples of classes include the Int or Float, as well as np.array or matplotlib plots
# defining your own classes is a powerful tool and the basis of OOP


class Vector:

    vector_count = 0 # this is a variable associated with the entire class

    def __init__(self, x, y): # this initialises a Vector object, which takes the inputs x and y
        self.x = x # this is personal and not shared with other objects
        self.y = y
        Vector.vector_count += 1 # this accesses the class variable
        self.id = Vector.vector_count


    def length(self) -> float:
        """this returns the length of the vector"""
        return np.sqrt(self.x**2 + self.y**2)
    

    def vector_add(self, other:"Vector") -> "Vector":
        """Adds two vectors together"""
        x = self.x + other.x
        y = self.y + other.y

        return(Vector(x,y))
    

    def invert(self) -> "Vector":
        """returns the inverse of the vector (does not alter in place)"""
        return Vector(-self.x, -self.y)

    def vector_subtract(self, other:"Vector") -> "Vector":
        """subtracts one vector from the other"""

        return self.vector_add(other.invert())
    
    def unit_vector(self) -> "Vector":
        """returns the normalised version of this vector"""
        length = self.length()
        x = self.x / length
        y = self.y / length
        return Vector(x,y)
    
    def reset(self) -> None:
        """resets the vector to 0,0. (returns nothing)"""

        self.x = 0
        self.y = 0
        return
    


# there's also dataclasses for easy creation of data classes:
# it automatically handles stuff like __init__ and __repr__

@dataclass
class Datapoint:
    X:float
    Y:float
    Z:float
    tow_width:float
    tow_center:float
    # etc.
    def tow_error(self): # but it still allows for methods if you need it
        return self.X + 0.5*self.tow_width - self.tow_center


# One useful way to use classes is to abstract or restrict data
class Thingimajig():
    """A class that does a bunch of stuff the end user shouldn't access"""

    name:str = "Thing" # class variable anyone can access
    _id:int = 1 # a private variable that other *can* access, but shouldn't
    __secret_code = 1234 # a private variable those outside the class can't access.


    def check_code(code):
        if code == Thingimajig.__secret_code:
            return True
        else:
            return False

    # the code can't be accessed outside the class

    def change_code(old_code, new_code):

        if Thingimajig.check_code(old_code):
            Thingimajig.__secret_code = new_code
    
    # but inside the class it can be changed or accessed (getters and setters)
    # the same can be done with other variables using @[parameter].setter if you want to "hide"
    # this behind the regular way to access stuff

    @property
    def id(self):
        return Thingimajig._id + 100 # means that using normal dot notation you get the id + 100

    @id.setter # might not work like this?
    def id(self, a):
        Thingimajig._id = a * 2 # means that setting the id makes it twice what you tried to input
        print("Someone changed the ID!") # you can also make other stuff happen in these functions


def main2():
    
    print(Thingimajig.name)
    try:
        print(Thingimajig.__secret_code)
    except AttributeError:
        print("Nope! can't edit that")
    foo = Thingimajig()
    foo.id = 5
    print(foo.id)



def main():
    # Here the code starts

    F = Vector(3,2) # X is now a "Vector" object, and was initialized with the values x = 3 and y = 2
    G = Vector(1,1) # G is also a vector with values x=1, y=1

    K = F.vector_add(G) # K is the vector resulting from the addition of F and G

    print(K.length()) # this prints 5

    print(K.id) # this prints 3
    Vector.vector_count = 50
    W = Vector(5,2)
    print(W.id) # this prints 51, since we changed the count
    W.vector_count = 5 # BEWARE! class varables are only accessed from the class
    V = Vector(2,2)
    print(V.id) # this prints 52, since the class varaible wasn't changed
    print(W.vector_count) # this however prints 5, since we overwrote the parameter on W
    W.color = "Green" # in python you can add new attributes (variables) whenever you like
    print(W.color) # prints Green, However don't do this as it becomes hard to track what attributes an object has
    try:
        print(K.color) # throws an error since K doesn't have a "color" attribute
    except AttributeError:
        print("K doesn't have a color")

    Vector.vector_count = 0
    print(Vector.vector_count) #now the count is zero again

    F.reset() # this doesn't change the count since we modify the object in place
    print(Vector.vector_count)  

    V = V.unit_vector() # This does however since the method returns a new vector
    print(Vector.vector_count)



if __name__ == "__main__":
    main()


'''
Another way to organise data which might be quicker is using Pandas
think of it like np.arrays or lists of lists,
it has some nice methods for joining, merging, and selecting parts of data
though we don't get the control of making our own classes

'''