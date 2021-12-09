from dataclasses import dataclass, field
from typing import Optional, Sequence, Set, TypeVar
from uuid import UUID

from backports.cached_property import cached_property

from .spec import Specification

UserId = TypeVar('UserId', int, str, UUID)


@dataclass(frozen=True)
class Client:
    user_id: UserId
    login: str
    name: str
    app_groups: Sequence["Group"] = field(default_factory=tuple)
    groups: Set[str] = field(default_factory=set)
    email: Optional[str] = None

    @classmethod
    def create(cls, **kwargs):
        prepared_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if 'groups' in prepared_kwargs and not isinstance(prepared_kwargs['groups'], set):
            groups = set()
            groups.update(prepared_kwargs['groups'])
            prepared_kwargs['groups'] = groups
        return cls(**prepared_kwargs)

    @cached_property
    def permissions(self) -> Set[str]:
        result = set()

        if not self.app_groups:
            return result

        for group in self.app_groups:
            if group.name in self.groups:
                result.update(map(lambda perm: perm.name, group.permissions))

        return result


@dataclass(frozen=True)
class Permission(Specification):
    name: str

    def is_satisfied_by(self, candidate: Client):
        return self.name in candidate.permissions


@dataclass(frozen=True)
class Group(Specification):
    name: str
    permissions: Sequence[Permission] = field(default_factory=tuple, hash=False, compare=False)

    def is_satisfied_by(self, candidate: Client):
        return self.name in candidate.groups
