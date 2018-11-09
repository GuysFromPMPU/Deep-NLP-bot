def get_info(request, response, user_storage):
    response.set_text('Жду когда меня запилит серега')
    return response, user_storage