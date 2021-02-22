from marshmallow import Schema, fields, validate

MALE = 'male'
FEMALE = 'female'
GENDERS = [MALE, FEMALE]


class MyProfileSchema(Schema):
    id = fields.Integer(dump_only=True)
    firstname = fields.String(
        required=False,
        validate=validate.Length(max=100)
    )
    surname = fields.String(
        required=False,
        validate=validate.Length(max=100)
    )
    user_id = fields.Integer(dump_only=True)
    birthdate = fields.Date(required=False)
    gender = fields.String(
        required=False,
        validate=validate.OneOf(choices=GENDERS)
    )
    avatar = fields.URL(
        required=False,
        validate=validate.Length(max=200)
    )

    class Meta:
        strict = True


class ProfileSchema(Schema):
    id = fields.Integer(dump_only=True)
    firstname = fields.String(
        required=False,
        validate=validate.Length(max=100)
    )
    surname = fields.String(required=False)
    user_id = fields.Integer(required=True)
    birthdate = fields.Date(required=False)
    gender = fields.String(
        required=False,
        validate=validate.OneOf(choices=GENDERS)
    )
    avatar = fields.URL(required=False)

    class Meta:
        strict = True


class Message(Schema):
    message = fields.String(
        dump_only=True,
        required=True
    )


profile_schema = ProfileSchema()
my_profile_schema = MyProfileSchema()


default_profile_responses = {
    400: {
      "description": "Response to all bad, malformed, unvalidated request",
      "schema": Message(),
      "examples": {
          "Duplicated key or id": {"message": "BadRequest: duplicate key value violates unique constraint"},
          "Validation errors": {"message": "ValidationError: {'birthdate': ['Not a valid date.']}"}
      }
    },
    401: {
        "description": "Unauthorized user response",
        "schema": Message(),
        "examples": {
            "No authorization": {"message": "HTTPUnauthorized: Authorization required"},
            "Expired token": {"message": "HTTPUnauthorized: Invalid authorization token, Signature has expired"}
        }
    },
    403: {
        "description": "HTTPForbidden: Invalid authorization header",
        "schema": Message(),
        "examples": {
            "Invalid token": {"message": "HTTPForbidden: Invalid authorization header"},
            "Not enough privileges": {"message": "HTTPForbidden: Insufficient scopes"}
        }
    },
    404: {
        "description": "RecordNotFound: Profile with user_id=%d is not found",
        "schema": Message(),
        "examples": {
            "Record not found": {"message": "RecordNotFound: Profile with user_id=%d is not found"}
        }
    },
    500: {"description": "Server error"},
}
