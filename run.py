
from nnf import Var

def theory():
    # Define Variables
    A, B, C = map(Var, 'abc')

    # TODO: Create a theory that matches (A ∨ B) ∧ (¬A ∨ C)
    pass

if __name__ == "__main__":
    print("Theory: " % str(theory()))
