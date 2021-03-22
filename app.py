"""
Flask backend with DynamoDB
Client -> Flask -> DynamoDB
"""
import boto3
import json
from flask import Flask
# from flask_cors import CORS, cross_origin
from flask import jsonify, request
# Add logging
# https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
import logging
from repository import DynamoDbCourseRepo
from uuid import uuid4

logger = logging.getLogger()
logger.setLevel(logging.INFO)
app = Flask(__name__)

repo = DynamoDbCourseRepo()

@app.route("/course", methods=["GET", "POST"])
def course():
    if request.method == "POST":
        body = request.json
        if body and "id" in body and "name" in body:
            id = body["id"]
            name = body["name"]
            if id and name:
                repo.create_or_replace_course(id, name)
                course = repo.get_course_by_id(id)
                return jsonify(course_id=course.id, name=course.name), 201 # created
        return "Invalid input", 400 # Bad Request

    elif request.method == "GET":
        id = request.args.get("id")
        if id:
            course = repo.get_course_by_id(id)
            return jsonify(course_id=course.id, name=course.name), 200
        else:
            return "Not Found", 404


@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        body = request.json
        if body and "name" in body:
            id = uuid4()
            name = body["name"]
            if name:
                repo.create_student(id, name)
                created = repo.get_student_by_id(id)
                return jsonify(student_id=id), 201 # created
        return "Invalid input", 400 # Bad Request

    elif request.method == "GET":
        id = request.args.get("id")
        if not id:
            return "Invalid request", 400
        stud = repo.get_student_by_id(id)
        if stud:
            return jsonify(id=stud.id, name=stud.name, courses=stud.courses), 200
        else:
            return "Not found", 404




@app.route("/professor", methods=["GET", "POST"])
def professor():
    if request.method == "POST":
        body = request.json
        if body and "name" in body:
            id = uuid4()
            name = body["name"]
            if name:
                repo.create_professor(id, name)
                created = repo.get_professor_by_id(id)
                return jsonify(professor_id=id), 201 # created
        return "Invalid input", 400 # Bad Request

    elif request.method == "GET":
        id = request.args.get("id")
        if id:
            prof = repo.get_professor_by_id(id)
            return jsonify(id=prof.id, name=prof.name, courses=prof.courses), 200
        else:
            return "Not Found", 404



@app.route("/register_student", methods=["POST"])
def register_student():
    body = request.json
    if body and "student_id" in body and "course_id" in body:
        student_id = body["student_id"]
        course_id = body["course_id"]

        if student_id and course_id:
            stud = repo.get_student_by_id(student_id)
            course = repo.get_course_by_id(course_id)
            if not stud:
                return "Student Not Found", 404
            if not course:
                return "Course Not Found", 404

            repo.register_student(stud, course)
            return "Registered", 200

    return "Invalid Input", 400 # Bad Request


@app.route("/assign_professor", methods=["POST"])
def assign_professor():
    body = request.json
    if body and "professor_id" in body and "course_id" in body:
        professor_id = body["professor_id"]
        course_id = body["course_id"]

        if professor_id and course_id:
            prof = repo.get_professor_by_id(professor_id)
            course = repo.get_course_by_id(course_id)
            if not prof:
                return "Professor Not Found", 404
            if not course:
                return "Course Not Found", 404

            repo.assign_professor(prof, course)
            return "Assigned", 200

    return "Invalid Input", 400  # Bad Request
