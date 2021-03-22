from dataclasses import dataclass


@dataclass
class Course:
    id: str
    name: str


@dataclass
class Student:
    id: str
    name: str
    courses: list


@dataclass
class Professor:
    id: str
    name: str
    courses: list

