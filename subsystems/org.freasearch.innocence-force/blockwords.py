def is_included_in_list(title, words_list):
    for detect_word in words_list:
        if detect_word in title:
            return True
        return False

def on_result(request, search, result):
    if parsed in result:
        result_title = result['title']
    else:
         return True

    detect_words_1=['コロナ', 'ワクチン', 'マスク']
    detect_words_2=['強制', '強要', '陰謀']
    block_words=['現役エンジニア', '徹底解説', '枠珍']

    if is_included_in_list(result_title, detect_words_1):
        if is_included_in_list(result_title, detect_words_2):
            return False
        else:
            return True
    elif is_included_in_list(result_title, block_words):
        return False
    else:
        return True
