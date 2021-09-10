from getFPathImage import *
from ams_s3 import *


db = database()
ams = Aws()
base = 'static'
base_url = 'http://127.0.0.1:8000'


def begin():

    list_subject_id = list()
    list_topic_id = list()
    list_document_id = list()
    list_name = list()

    list_doc = list()
    list_subject = os.listdir(base)
    for subjec in list_subject:
        list_topic = os.listdir(base + '/' + subjec)
        list_subject_id.append(db.insert_one('subject', subjec))
        for topic in list_topic:
            list_doc_question = os.listdir(f'{base}/{subjec}/{topic}')
            list_topic_id.append(db.insert_one('topic', topic))
            list_doc += get_list_doc(list_doc_question)
            list_doc = clear_duplicate(list_doc)

    for doc in list_doc:
        list_document_id.append(db.insert_one('document', doc))


def get_data():
    list_subject = db.select_all('subject')
    list_topic = db.select_all('topic')
    list_doc = db.select_all('document')
    list_topic_id = list()
    for i in list_topic:
        list_topic_id.append(i[0])
    db.create_point_detail(list_topic_id)

    list_question_id = list()
    for subjec in list_subject:
        for topic in list_topic:
            try:
                list_doc_question = os.listdir(f"{base}/{subjec[1]}/{topic[1]}")
                for doc_and_file in list_doc_question:
                    if is_file(doc_and_file) and is_question(doc_and_file):
                        doc = ''
                        if is_multi_choice(doc_and_file):
                            type = 'multi choice'
                        if is_long_response(doc_and_file):
                            type = 'long response'

                        url = ams.upload_file(f'{base}/{subjec[1]}/{topic[1]}/{doc_and_file}')
                        if type == 'long response':
                            try:
                                a = ams.upload_file(
                                    ams.upload_file(f'{base}/{subjec[1]}/{topic[1]}/{doc_and_file[: -4]}M.png')
                                )
                            except:
                                pass
                        db.insert_one_question(
                            subject=subjec[0],
                            topic=topic[0],
                            document=doc,
                            question=convert_question_name(doc_and_file),
                            type=type,
                            link=url
                        )

                    if not is_file(doc_and_file):
                        for i in list_doc:
                            if doc_and_file == i[1]:
                                doc_and_file = i[1]
                                id_doc = i[0]
                            list_question = os.listdir(f'{base}/{subjec[1]}/{topic[1]}/{doc_and_file}')
                            for question in list_question:
                                if is_file(question) and is_question(question):
                                    if is_multi_choice(question):
                                        type = 'multi choice'
                                    if is_long_response(question):
                                        type = 'long response'
                                    url = ams.upload_file(f'{base}/{subjec[1]}/{topic[1]}/{doc_and_file}/{question}')
                                    if type == 'long response':
                                        try:
                                            a = ams.upload_file(
                                                f'{base}/{subjec[1]}/{topic[1]}/{doc_and_file}/{question[:-4]}M.png'
                                            )
                                        except:
                                            pass

                                    db.insert_one_question(
                                        subject=subjec[0],
                                        topic=topic[0],
                                        document=get_id_by_name(doc_and_file, list_doc),
                                        question=convert_question_name(question),
                                        type=type,
                                        link=url
                                    )
            except:
                pass

    ams.set_public()


def get_id_by_name(name, list_data):
    for data in list_data:
        if data[1] == name:
            return data[0]
    return None


if __name__ == '__main__':
    db.create_database()
    begin()
    get_data()
    db.insert_one_row('account', username=20160320, password='1')
    db.insert_one_row('point', user=1, point=0)
    db.insert_one_row('point_detail', user=1, topic_1=0)