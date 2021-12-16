"""
Taken from here https://gist.github.com/palankai/f73a18ce06751ab8f245
"""

from abc import ABC


class Specification(ABC):
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __xor__(self, other):
        return Xor(self, other)

    def __invert__(self):
        return Invert(self)

    def is_satisfied_by(self, candidate):
        raise NotImplementedError()

    def remainder_unsatisfied_by(self, candidate):
        if self.is_satisfied_by(candidate):
            return None
        else:
            return self


class CompositeSpecification(Specification, ABC):
    pass


class MultaryCompositeSpecification(CompositeSpecification, ABC):
    def __init__(self, *specifications):
        self.specifications = specifications


class And(MultaryCompositeSpecification):
    def __and__(self, other):
        if isinstance(other, And):
            self.specifications += other.specifications
        else:
            self.specifications += (other, )
        return self

    def is_satisfied_by(self, candidate):
        satisfied = all(
            [specification.is_satisfied_by(candidate) for specification in self.specifications]
        )
        return satisfied

    def remainder_unsatisfied_by(self, candidate):
        non_satisfied = [
            specification for specification in self.specifications
            if not specification.is_satisfied_by(candidate)
        ]
        if not non_satisfied:
            return None
        if len(non_satisfied) == 1:
            return non_satisfied[0]
        if len(non_satisfied) == len(self.specifications):
            return self
        return And(*non_satisfied)


class Or(MultaryCompositeSpecification):
    def __or__(self, other):
        if isinstance(other, Or):
            self.specifications += other.specifications
        else:
            self.specifications += (other, )
        return self

    def is_satisfied_by(self, candidate):
        satisfied = any(
            [specification.is_satisfied_by(candidate) for specification in self.specifications]
        )
        return satisfied


class UnaryCompositeSpecification(CompositeSpecification, ABC):
    def __init__(self, specification):
        self.specification = specification


class Invert(UnaryCompositeSpecification):
    def is_satisfied_by(self, candidate):
        return not self.specification.is_satisfied_by(candidate)


class BinaryCompositeSpecification(CompositeSpecification, ABC):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Xor(BinaryCompositeSpecification):
    def is_satisfied_by(self, candidate):
        return self.left.is_satisfied_by(candidate) ^ self.right.is_satisfied_by(candidate)
