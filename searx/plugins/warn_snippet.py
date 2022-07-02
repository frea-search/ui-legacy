name = "Warning snippet"
description = "Displays advice and warnings."
default_on = True

def post_search(request, search):
    if search.search_query.pageno > 1:
        return True
    if 'コロナ' in search.search_query.query:
        message = "新型コロナウイルス感染症や新型コロナウイルスワクチンに関する正しい情報をお求めの場合は、WHOのページをご確認ください。"
    search.result_container.answers['warning'] = {'answer': message}
    return True