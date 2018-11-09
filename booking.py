from answers import get_replica

composers = [
    "Рахманинов", 
    "Чайковский"
]

def select_composer(response, user_storage, tag):
    select_text = get_replica(tag)
    response.set_text(select_text) 
    response.set_variants(*composers)
    return response, user_storage


def book(request, response, user_storage):
    user_storage.setdefault("buying", True)

    if "composer" not in user_storage:
        user_storage["composer"] = False
        return select_composer(response, user_storage, "select-composer")

    if not user_storage["composer"]:
        for composer in composers:
            if (request.has_lemmas(composer)):
                user_storage["composer"] = composer
                break
        else:
            return select_composer(response, user_storage,"select-composer-unknown")


       
    response.set_text(f"Ты выбрал {user_storage['composer']}")

    return response, user_storage
