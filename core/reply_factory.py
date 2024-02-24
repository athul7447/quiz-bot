
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    try:
        #validating the answer
        if len(answer) == 0:
            return False, "Please provide a answer."
        
        answer_list_data = session.get("answers_list",{})
        
        #set current question answer to a dictionary
        answer_list_data[str(current_question_id)] = answer
            
        
        #saving the answer to django session 
        session['answers_list'] =  answer_list_data
        session.save()
        
        return True, ""
    except:
        return False,"Something went wrong!"


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question = None
    
    #get the next question id
    if not current_question_id:
        next_question_id = 0
    else:
        next_question_id = current_question_id + 1
    
    #get the question using question id
    try:
        next_question_data = PYTHON_QUESTION_LIST[next_question]
        next_question = next_question_data['question_text']
    except IndexError:
        pass
    
    #setting curre_question id in next question id if there is no newt question
    if not next_question:
        next_question_id = current_question_id

    return next_question, next_question_id


def generate_final_response(session):
    #get all answer data from session
    all_answers = session.get('answers_list',{})
    
    #if there is not aswers in session trowing error
    if len(all_answers) == 0:
        return "No answers are found. Please try again later."
    
    total_questions = len(PYTHON_QUESTION_LIST)
    total_answers = len(all_answers)
    
    right_answers = 0
    #valuation of answer
    right_answers = sum(1 for question_id, current_answer in all_answers.items()
                       if current_answer == PYTHON_QUESTION_LIST[question_id]['answer'])
    

    return f"You got {right_answers}/{total_questions} right."
