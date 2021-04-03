# Academic Registration System
POC that simulates an academic class registration system

Flask application, that, when runs, will allow users to interact with and populate an academic class registration system based on the 
below requirements.

# Requirements:
1. Create a simple API that implements an academic class registration system with REST endpoints that provide the below features. A UI is not needed.
2. Create Courses
3. Create Professors
4. Assign Professors to Courses
5. Create Students
6. Students register for Courses
7. The system should operate over long periods of time
8. The system should be able to scale to 200 requests per second efficiently.
9. We should have access to the source code in an online repository
10. The application should run in the cloud
11. No restrictions on technologies. AWS technologies would be preferred, but not required.
12. Data should be persisted in some form of database.
13. We do not expect that you spend more than 8 hours on this challenge, so some rough edges
are acceptable.
14. Treat this as a proof of concept, so documentation is not important.


# Endpoints:

If testing this locally with postman for example, these endpoints will be appended to localhost...

/course: supports both GET(id) and POST(id and name)

/student: supports both GET(id) and POST(name)

/professor: supports both GET(id) and POST(name)

/register_student: supports POST(student_id and course_id)

/assign_professor:supports POST(professor_id and course_id)
