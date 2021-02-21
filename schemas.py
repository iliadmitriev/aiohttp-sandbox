from marshmallow import Schema, fields, validate


MALE = 'male'
FEMALE = 'female'
GENDERS = [MALE, FEMALE]


class ProfileSchema(Schema):
    id = fields.Integer(dump_only=True)
    firstname = fields.String(required=False)
    surname = fields.String(required=False)
    user_id = fields.Integer(required=True)
    birthdate = fields.Date(required=False)
    gender = fields.String(
        required=False,
        validate=validate.OneOf(choices=GENDERS)
    ),
    avatar = fields.URL(required=False)


profile_schema = ProfileSchema()
