from account_api import db
from datetime import datetime
import datetime
import uuid
from sqlalchemy.dialects.postgresql import JSONB


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.String(36), primary_key=True)
    full_name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow(),  nullable=False)
    house_number = db.Column(db.String(64))
    house_type = db.Column(db.String(64))
    street = db.Column(db.String(64))
    postcode = db.Column(db.String(64))
    latitude = db.Column(db.String(300))
    longitude = db.Column(db.String(300))
    uprn = db.Column(db.String(300))
    headingvaluefound = db.Column(db.String(300))
    headervalue = db.Column(db.String(300))

    creation_status = db.Column(db.String(64), default='pending')
    creation_start = db.Column(db.DateTime, nullable=True)
    report_data_stored = db.Column(db.Boolean, default=False)
    report_data = db.Column(JSONB, nullable=True)

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "timestamp": self.timestamp,
            "house_number": self.house_number,
            "house_type": self.house_type,
            "street": self.street,
            "postcode": self.postcode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "uprn": self.uprn,
            "headingvaluefound": self.headingvaluefound,
            "headervalue": self.headervalue,
            "payment_status": self.get_payment_status(),
            "creation_status": self.creation_status,
            "creation_start": self.creation_start,
            "report_data_stored": self.report_data_stored,
        }

    def get_payment_status(self):
        # get most recent payment
        payment = Payment.query.filter(Payment.report_id == self.id).order_by(Payment.timestamp.desc()).first()

        if payment:
            return payment.status
        else:
            return 'unpaid'

    def get_report_data(self):
        return self.report_data

    @classmethod
    def create_report(cls, data):
        report = cls(
            id=str(uuid.uuid4()),
            full_name=data.get('full_name'),
            email=data.get('email'),
            house_number=data.get('house_number'),
            house_type=data.get('house_type'),
            street=data.get('street'),
            postcode=data.get('postcode'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            uprn=data.get('uprn'),
            headingvaluefound=data.get('headingvaluefound'),
            headervalue=data.get('headervalue'),
        )
        report.save()
        return report

    @classmethod
    def get_report_by_id(cls, report_id):
        return cls.query.filter(cls.id == report_id).first()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.save()
        return self


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.String(36), primary_key=True)
    report_id = db.Column(db.String(36), db.ForeignKey('reports.id'))
    status = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow(),  nullable=False)

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "report_id": self.report_id,
            "status": self.status,
            "timestamp": self.timestamp
        }

    @classmethod
    def create_payment(cls, data):
        payment = cls(
            id=data.get('id'),
            report_id=data.get('report_id', None),
            status=data.get('status')
        )
        payment.save()
        return payment

    @classmethod
    def get_payment_by_id(cls, payment_id):
        return cls.query.filter(cls.id == payment_id).first()

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.save()
        return self
