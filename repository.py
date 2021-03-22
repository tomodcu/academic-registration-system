import boto3
from models.model import *

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class CourseManagementRepo:
    def create_or_replace_course(self, id, name):
        raise NotImplementedError()

    def get_course_by_id(self, id) -> Course:
        raise NotImplementedError()

    def create_student(self, id, name):
        raise NotImplementedError()

    def get_student_by_id(self, id) -> Student:
        raise NotImplementedError()

    def get_professor_by_id(self, id) -> Professor:
        raise NotImplementedError()

    def create_professor(self, id, name):
        raise NotImplementedError()

    def register_student(self, student_id, course):
        raise NotImplementedError()

    def assign_professor(self, professor_id, course):
        raise NotImplementedError()


_COURSE_TABLE = "Course"
_STUDENT_TABLE = "Student"
_PROFESSOR_TABLE = "Professor"


class DynamoDbCourseRepo(CourseManagementRepo):

    def __init__(self, client=None):
        if not client:
            client = boto3.client("dynamodb")
        self.client = client

    def create_or_replace_course(self, id, name):
        self.client.put_item(
            TableName=_COURSE_TABLE,
            Item=dict(
                id={"S": str(id)},
                name={"S": name}
            )
        )

    def get_course_by_id(self, id) -> Course:
        course = self.client.get_item(
            TableName=_COURSE_TABLE,
            Key=dict(
                id={"S": str(id)}
            )
        )
        if "Item" in course:
            item = course["Item"]
            return Course(
                id=item["id"]["S"],
                name=item["name"]["S"],
            )

    def create_student(self, id, name):
        self.client.put_item(
            TableName=_STUDENT_TABLE,
            Item=dict(
                id={"S": str(id)},
                name={"S": name}
            )
        )

    def get_student_by_id(self, id) -> Student:
        stud = self.client.get_item(
            TableName=_STUDENT_TABLE,
            Key=dict(
                id={"S": str(id)}
            )
        )
        if "Item" in stud:
            item = stud["Item"]
            if "courses" in item:
                courses = item["courses"]["L"]
                courses = [Course(id=c["M"]["course_id"]["S"], name=c["M"]["name"]["S"]) for c in courses]
            else:
                courses = []
            return Student(
                id=item["id"]["S"],
                name=item["name"]["S"],
                courses=courses
            )

    def get_professor_by_id(self, id) -> Professor:
        prof = self.client.get_item(
            TableName=_PROFESSOR_TABLE,
            Key=dict(
                id={"S": str(id)}
            )
        )
        if "Item" in prof:
            item = prof["Item"]
            if "courses" in item:
                courses = item["courses"]["L"]
                courses = [Course(id=c["M"]["course_id"]["S"], name=c["M"]["name"]["S"]) for c in courses]
            else:
                courses = []
            return Professor(
                id=item["id"]["S"],
                name=item["name"]["S"],
                courses=courses
            )

    def create_professor(self, id, name):
        self.client.put_item(
            TableName=_PROFESSOR_TABLE,
            Item=dict(
                id={"S": str(id)},
                name={"S": name}
            )
        )

    def register_student(self, student: Student, course: Course):
        courses = student.courses + [course]

        self.client.put_item(
            TableName=_STUDENT_TABLE,
            Item=dict(
                id={"S": str(student.id)},
                name={"S": student.name},
                courses={"L": [{"M": {"course_id": {"S": c.id}, "name": {"S": c.name}}} for c in courses]}
            )
        )

    def assign_professor(self, prof: Professor, course: Course):
        courses = prof.courses + [course]

        self.client.put_item(
            TableName=_PROFESSOR_TABLE,
            Item=dict(
                id={"S": str(prof.id)},
                name={"S": prof.name},
                courses={"L": [{"M": {"course_id": {"S": c.id}, "name": {"S": c.name}}} for c in courses]}
            )
        )
