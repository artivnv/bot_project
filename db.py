from pymongo import MongoClient
import settings

db = MongoClient(settings.MONGODB_HOST)[settings.MONGODB_DB]

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


def save_vote_for_reports(db, context, update, callback_query, effective_user):
    vote = db.vote_for_reports.find_one({"user_id": effective_user.id})
    if not vote:
        vote = {
            "user_id": effective_user.id,
            "username": context.callback_query.message.chat.username,
            "name_report_0": context.callback_query.message.text,
            "grades_report_0": context.callback_query.data,
            "name_report_1": context.callback_query.message.text,
            "grades_report_1": context.callback_query.data,
            "name_report_2": context.callback_query.message.text,
            "grades_report_2": context.callback_query.data

        }
        db.vote_for_reports.insert_one(vote)
    return vote








