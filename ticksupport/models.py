"""Data models."""
from . import db


class support_ticket(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'support_tickets'
    id = db.Column(
        db.Integer,
        primary_key=True,
        auto_increment=True
    )
    client = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    issue = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    status = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    assigned = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    log = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    deadline = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=True
    )

    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    last_update = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<suppoer_ticket {}>'.format(self.id)
