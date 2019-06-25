from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


db = SQLAlchemy()




# *************************        CLIENT TABLE         *******************************
# *************************************************************************************
class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, primary_key=True, default=None)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, default=None, nullable=False)
    password = db.Column(db.String(120), unique=True, default=None, nullable=False)
    client_login_status = db.Column(db.Boolean(), default=False)

    orders_id = db.Column(Integer, ForeignKey('orders.id'))
    service_catalog_id = db.Column(Integer, ForeignKey('service_catalog.id'))
    # orders = relationship("Orders")
    # orders = relationship("Orders", back_populates="Client")

    def __repr__(self):
        return '<Client %r>' % self.email

    def serialize(self):
        return {
            "client_id": self.client_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "client_login_status": self.client_login_status
        }




# *************************        ORDERS TABLE         *******************************
# *************************************************************************************
class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=True, default=None)
    client_email = db.Column(db.String(120), nullable=True, default=None)
    meeting_type = db.Column(db.String(120), nullable=True, default=None)
    discount = db.Column(db.Integer, nullable=True, default=None)
    payment_type = db.Column(db.String(120), nullable=True, default=None)
    payment_status = db.Column(db.String(120), nullable=True, default=None)
    order_status = db.Column(db.String(20), default = 'Open', nullable=True)
    order_notes = db.Column(db.String(5000), nullable=True, default=None)
    order_issues = db.Column(db.String(5000), nullable=True, default=None)
    date_completed = db.Column(db.DateTime, nullable=True, default=None)
    total = db.Column(db.Integer, nullable=True, default=None)
    # order_number = db.Column(db.Integer, nullable=True, default=None)
    # selected_services = db.Column(db.String(5000), nullable=True, default=None)
    # assigned_consultant = db.Column(db.String(120), nullable=True, default=None)

    # consultants = relationship('consultants')
    # services = relationship('services')
    service_catalog_id = db.Column(Integer, ForeignKey('service_catalog.id'))
    client_id = db.Column(Integer, ForeignKey('client.client_id'))

    def __repr__(self):
        return '<Orders %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "order_status": self.order_status,
            "total": self.total
            # "order_number": self.order_number,
            # "assigned_consultant": self.assigned_consultant,
            # "selected_services": self.selected_services,
        }




# ************************        SERVICES TABLE         ******************************
# *************************************************************************************
class Service_catalog (db.Model):
    __tablename__ = 'service_catalog'
    id = db.Column(db.Integer, primary_key=True)
    assigned_consultant = db.Column(db.String(120), nullable=True, default=None)
    service = db.Column(db.String(120), nullable=True, default=None)
    description = db.Column(db.String(5000), nullable=True, default=None)
    price = db.Column(db.Integer, nullable=True, default=None)

# Alejandro suggested making "service_type" (to specify if its from "Strategy", "Identity", or "Marketing") an Enum; but I couldn't figure out the proper syntax for it- even after googling it.
    service_type = db.Column(db.String(5000), nullable=True, default=None)
# Alejandro suggested making "package" a boolean; but I couldn't figure out how to write it, regarding syntax - even after googling it.
    package = db.Column(db.String(5000), nullable=True, default=None)

    orders_id = db.Column(Integer, ForeignKey('orders.id'))
    client_id = db.Column(Integer, ForeignKey('client.client_id'))

    def __repr__(self):
        return '<service_catalog %r>' % self.service

    def serialize(self):
        return {
            "id": self.id,
            "service": self.service,
            "assigned_consultant": self.assigned_consultant,
            "service_type": self.service_type,
            "price": self.price
        }