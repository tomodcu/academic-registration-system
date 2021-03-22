from app import app

import json
import unittest


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.tc = app.test_client()

    def _create(self, entity, name, id=None):
        data = dict(name=name)
        if id:
            data["id"] = id

        response = self.tc.post(
            f"/{entity}",
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        entity_id = response.json[f"{entity}_id"]

        return entity_id

    def test_create_and_get_student(self):
        id = self._create("student", "Tom")

        response = self.tc.get(f'/student?id={id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["courses"], [])
        self.assertEqual(response.json["name"], "Tom")

    def test_create_and_get_professor(self):
        id = self._create("professor", "Prof1")

        response = self.tc.get(f'/professor?id={id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["courses"], [])
        self.assertEqual(response.json["name"], "Prof1")

    def test_create_and_get_course(self):
        id = self._create("course", "Computer Science", "CS101")

        response = self.tc.get(f'/course?id=CS101')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Computer Science")

    def test_register_student(self):
        student_id = self._create("student", "Stud1")
        self._create("course", "Computer Science", "CS101")

        response = self.tc.post(
            f"/register_student",
            data=json.dumps(dict(student_id=student_id, course_id="CS101")),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        response = self.tc.get(f'/student?id={student_id}')
        self.assertEqual(response.json["courses"], [dict(id="CS101", name="Computer Science")])

        # Register a second course
        self._create("course", "Maths", "M101")
        response = self.tc.post(
            f"/register_student",
            data=json.dumps(dict(student_id=student_id, course_id="M101")),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        response = self.tc.get(f'/student?id={student_id}')
        self.assertEqual(response.json["courses"], [dict(id="CS101", name="Computer Science"),
                                                    dict(id="M101", name="Maths")])


    def test_assign_professor(self):
        prof_id = self._create("professor", "Prof1")
        self._create("course", "Computer Science", "CS101")

        response = self.tc.post(
            f"/assign_professor",
            data=json.dumps(dict(professor_id=prof_id, course_id="CS101")),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        response = self.tc.get(f'/professor?id={prof_id}')
        self.assertEqual(response.json["courses"], [dict(id="CS101", name="Computer Science")])

        # Register a second course
        self._create("course", "Maths", "M101")
        response = self.tc.post(
            f"/assign_professor",
            data=json.dumps(dict(professor_id=prof_id, course_id="M101")),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        response = self.tc.get(f'/professor?id={prof_id}')
        self.assertEqual(response.json["courses"], [dict(id="CS101", name="Computer Science"),
                                                    dict(id="M101", name="Maths")])


if __name__ == "__main__":
    unittest.main()
