from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# CATEGORY TABLE
# One category can have many threat records
class ThreatCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)

    threats = db.relationship("ThreatIntel", backref="category", lazy=True)


# MAIN THREAT INTELLIGENCE TABLE
class ThreatIntel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    threat_name = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(100))
    severity = db.Column(db.String(50))

    # Foreign key linking each threat to one category
    category_id = db.Column(db.Integer, db.ForeignKey("threat_category.id"))