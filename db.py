from pymongo import MongoClient
import settings

db = MongoClient(settings.MONGODB_HOST)[settings.MONGODB_DB]
db_flask = MongoClient(settings.MONGODB_HOST_FLASK)[settings.MONGODB_DB_FLASK]

def get_or_create_user(db, effective_user, message):
    user = db.bot_users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": message.chat.id
        }
        db.bot_users.insert_one(user)
    return user

def toggle_subscription(db, user_data):
    if not user_data.get('subscribed'):
        user_data['subscribed'] = True
    else:
        user_data['subscribed'] = False
    db.bot_users.update_one(
        {'_id': user_data['_id']},
        {'$set': {'subscribed': user_data['subscribed']}}
    )

def get_subscribers(db):
    return db.bot_users.find({'subscribed': True})

def save_assessment(db, effective_user, context):
    assessment = db.assessments.find_one({"user_id": effective_user.id})
    if not assessment:
        assessment = {
            "user_id": effective_user.id,
            "username": effective_user.username,
            "user_name": context['user_name'],
            "job": context['job'],
            "poz": context['poz'],
            "org_rating": context['org_rating'],
            "org_comment": context['org_comment']
        }
        db.assessments.insert_one(assessment)
    return assessment


def list_of_reports(update, context):
    obj = db_flask.event.find_one()
    from handlers import get_keyboard
    update.message.reply_text(obj['list_reports'], reply_markup=get_keyboard())










