from getFPathImage import database
import json


def get_all_question():
    db = database()
    data = db.select_all('question')
    data = json.dumps(data)
    return data


def get_all_topic():
    db = database()
    data = db.select_all('topic')
    data = json.dumps(data)
    return data


def get_all_document():
    db = database()
    data = db.select_all('document')
    data = json.dumps(data)
    return data


def get_point_db(id_student):
    db = database()
    point = db.select_one('point', id_student)[0][2]
    point_detail = db.select_one('point_detail', id_student)[0][0]
    return {'point': point, 'point_detail': point_detail}


def check_ans_and_update_row(id_student, result_student, id_question):
    db = database()
    answer = db.select_one('question', id_question)[0][6][-5: -4]
    point = int(get_point(id_student))
    if result_student == answer:
        point += 1
    db.update_one_row_by_field('point', 'user', 1, point=point)
    # list_result = db.select_one_by_fields('point_detail', 'user', 1)
    id_topic = db.select_one('question', id_question)[0][2]
    if id_topic == 1:
        db.update_one_row_by_field('point_detail', 'user', 1, topic_1=point)
    # if have_topic_field_in_result(list_result, id_topic):
    #     db.update_one_row_two_fields('point_detail', 'user', 1, 'detail', id_topic, point=point)


def have_topic_field_in_result(list_result, id_topic):
    for i in list_result:
        if i[-1] == id_topic:
            return True
    return False


def check_user_and_pass(user, passw):
    result = {
        'result': False,
        'id': None,
    }
    db = database()
    pas = db.select_one_by_fields('account', 'username', user)
    if str(passw) == str(pas[0][2]):
        result['result'] = True
        result['id'] = pas[0][0]
    return result
# check_ans_and_insert_row(1, 'C', 26)
#
# def test(table_name, key, value, **kwargs):
#     update = ''
#     i = 1
#     for k, v in kwargs.items():
#         if i < len(kwargs):
#             update += f'`{k}` = {v},  '
#         else:
#             update += f'`{k}` = {v}'
#         i += 1
#
#     sql = f'UPDATE `{table_name}` SET  {update} WHERE  `{key}` = {value} '
#     print(sql)
#
#
# test('test', key='bang', value=65, point=4)