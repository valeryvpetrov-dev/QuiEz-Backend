"""
Separate script for generating feedback questions - answers.

* Run it after migrations and before application use.

    $ ./manage.py shell
    >> exec(open('quiez/rest_api/prerequisites.py').read())
"""
from quiez.rest_api.models.question import QuestionFeedback
from quiez.rest_api.models.answer import QuestionFeedbackAnswer


def generate_feedback_questions() -> None:
    """
    Generates feedback questions.

    :return: None (feedback questions will be created).
    """
    if len(QuestionFeedback.objects.all()) < 4:
        _generate_feedback_questions()


def _bind_answers(question_feedback, list_str_answers: list) -> None:
    """
    Binds answers with corresponding question feedback instance.

    :param question_feedback: question feedback instance.
    :param list_str_answers: list of answers to bind.
    :return:
    """
    for str_answer in list_str_answers:
        QuestionFeedbackAnswer.objects.create(question_feedback=question_feedback, content=str_answer)


def _generate_feedback_questions() -> None:
    data = {
        "description": "Вам понравилось?",
        "type": "one",
    }
    list_str_answers = [
        "Да",
        "Нет"
    ]
    tuple_question_like = QuestionFeedback.objects.get_or_create(**data)
    if tuple_question_like[1]:
        _bind_answers(tuple_question_like[0], list_str_answers)

    data['description'] = "Выберите качества, характеризующие выступающего."
    data['type'] = "many"
    list_str_answers = [
        "Юмор",
        "Компетенция",
        "Красноречие",
        "Взаимодействие с аудиторией"
    ]
    tuple_question_good_points = QuestionFeedback.objects.get_or_create(**data)
    if tuple_question_good_points[1]:
        _bind_answers(tuple_question_good_points[0], list_str_answers)

    data['description'] = "Ваши впечатления?"
    data['type'] = "many"
    list_str_answers = [
        "Занимательно",
        "Скучно",
        "Информативно",
        "Неинформативно",
        "Непонятно",
        "Доходчиво",
    ]
    tuple_question_general_impression = QuestionFeedback.objects.get_or_create(**data)
    if tuple_question_general_impression[1]:
        _bind_answers(tuple_question_general_impression[0], list_str_answers)


generate_feedback_questions()
