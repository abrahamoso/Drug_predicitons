from marshmallow import Schema, fields

class DrugRequestSchema(Schema):
    drug_names = fields.List(fields.Str(), required=True)
    drug_name = fields.Str()
    updated_info = fields.Dict()
