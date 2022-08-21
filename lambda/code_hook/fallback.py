import dialogstate_utils as dialog
import random
from prompts_responses import Prompts

engaging_prompts = [
    "Todavía estoy aquí", "Continúa", " ", "Estoy escuchando",
     "¿Qué más puedo hacer por ti?"]
did_not_follow_prompts = [
    "No entendí", "No entendí eso",
     "No entendí lo que dijiste."]

def not_meaningful(user_utterance):
    if user_utterance == '' or len(user_utterance) < 3:
        return True
    return False    
    
def handler(intent_request):
    intent = dialog.get_intent(intent_request)
    user_utterance = intent_request['inputTranscript']
    active_contexts = dialog.get_active_contexts(intent_request)
    session_attributes = dialog.get_session_attributes(intent_request)
    prompts = Prompts('fallback')
    
    if not_meaningful(user_utterance):
        return dialog.elicit_intent(
            active_contexts, session_attributes, intent, 
            [{'contentType': 'PlainText', 'content': 
                random.choice(engaging_prompts)}])
    
    interpreted_intents = dialog.get_interpreted_intents(intent_request)
    possible_intents = interpreted_intents[1:]
    
    default_fallback_message = random.choice(did_not_follow_prompts) \
+"Algunas de las cosas en las que puedo ayudarte son: \
                             Agendar una cita, \
                             hablar con un agente \
                             Ahora, ¿puede reformular su solicitud? "
    message = default_fallback_message
    if len(possible_intents) > 0:
        nearest_intent = possible_intents[0]
        if nearest_intent.get('nluConfidence') > 0.6:
            try:
                message = prompts.get(nearest_intent['name']) \
                            or default_fallback_message
            except:
                message = default_fallback_message
    
    return dialog.elicit_intent(
        active_contexts, session_attributes, intent, 
        [{'contentType': 'PlainText', 'content': message}])
    