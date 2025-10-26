#!/usr/bin/env python3
"""
Email tracking system for monitoring email delivery status
"""

from database import db
from datetime import datetime

class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    email_type = db.Column(db.String(50), nullable=False)  # 'welcome', 'admin_notification', 'test'
    status = db.Column(db.String(20), nullable=False)  # 'sent', 'failed'
    error_message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class EmailTracker:
    @staticmethod
    def log_email_sent(recipient_email, subject, email_type, user_id=None):
        """Log successful email sending"""
        try:
            email_log = EmailLog(
                recipient_email=recipient_email,
                subject=subject,
                email_type=email_type,
                status='sent',
                user_id=user_id
            )
            db.session.add(email_log)
            db.session.commit()
            return email_log.id
        except Exception as e:
            print(f"Error logging email success: {e}")
            return None
    
    @staticmethod
    def log_email_failed(recipient_email, subject, email_type, error_message, user_id=None):
        """Log failed email sending"""
        try:
            email_log = EmailLog(
                recipient_email=recipient_email,
                subject=subject,
                email_type=email_type,
                status='failed',
                error_message=str(error_message),
                user_id=user_id
            )
            db.session.add(email_log)
            db.session.commit()
            return email_log.id
        except Exception as e:
            print(f"Error logging email failure: {e}")
            return None
    
    @staticmethod
    def get_recent_emails(limit=50):
        """Get recent email logs"""
        return EmailLog.query.order_by(EmailLog.sent_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_email_stats():
        """Get email statistics"""
        total_emails = EmailLog.query.count()
        sent_emails = EmailLog.query.filter_by(status='sent').count()
        failed_emails = EmailLog.query.filter_by(status='failed').count()
        
        # Recent emails (last 24 hours)
        from datetime import timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_emails = EmailLog.query.filter(EmailLog.sent_at >= yesterday).count()
        
        return {
            'total': total_emails,
            'sent': sent_emails,
            'failed': failed_emails,
            'success_rate': (sent_emails / total_emails * 100) if total_emails > 0 else 0,
            'recent_24h': recent_emails
        }