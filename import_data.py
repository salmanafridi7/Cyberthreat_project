import pandas as pd

from app import app
from models import db, ThreatIntel, ThreatCategory


# Reading CSV file
threats_df = pd.read_csv("data/1_otx_threat_intel.csv")


with app.app_context():

    # Clear old records before importing again
    ThreatIntel.query.delete()
    ThreatCategory.query.delete()

    # Create categories
    malware = ThreatCategory(category_name="Malware")
    phishing = ThreatCategory(category_name="Phishing")
    suspicious = ThreatCategory(category_name="Suspicious Activity")

    db.session.add(malware)
    db.session.add(phishing)
    db.session.add(suspicious)
    db.session.commit()

    categories = [malware, phishing, suspicious]

    # Import threat records and link each threat to a category
    for index, row in threats_df.iterrows():

        category = categories[index % len(categories)]

        threat = ThreatIntel(
            threat_name=str(row.iloc[0]),
            source="OTX",
            severity="High",
            category_id=category.id
        )

        db.session.add(threat)

    db.session.commit()


print("Threat data with linked categories imported successfully!")