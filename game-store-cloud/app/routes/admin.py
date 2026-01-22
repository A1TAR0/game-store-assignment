from flask import Blueprint, render_template
from app.utils.db_sql import get_sql_connection

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users')
def list_users():
    """List all users - DEV ONLY"""
    conn = get_sql_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """SELECT user_id, email, username, created_at, last_login 
           FROM users ORDER BY created_at DESC"""
    )
    
    users = []
    for row in cursor.fetchall():
        users.append({
            'user_id': row[0],
            'email': row[1],
            'username': row[2],
            'created_at': row[3],
            'last_login': row[4]
        })
    
    cursor.close()
    conn.close()
    
    return render_template('admin/users.html', users=users)