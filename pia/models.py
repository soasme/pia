# -*- coding: utf-8 -*-

from datetime import datetime

from rio.core import db

class Program(db.Model):

    __table_name__ = 'pia_program'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'slug', name='ux_program_user_slug'),
    )

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    slug = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

class User(db.Model):

    __table_name__ = 'pia_user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

class Env(db.Model):

    __table_name__ = 'pia_env'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(2048), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
