from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# contains definitions of tables and associated schema constructs
metadata = MetaData()

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# define a model class by inheriting from db.Model.
