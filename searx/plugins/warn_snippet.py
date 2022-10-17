# SPDX-License-Identifier: AGPL-3.0-or-later

name = "Warning snippet"
description = "Displays advice and warnings."
default_on = True

def post_search(request, search):
    if search.search_query.pageno > 1:
        return True
    if 'コロナ' in search.search_query.query:
        message = "新型コロナウイルス感染症に関する正しい情報をお求めの場合は、厚生労働省のwebサイトをご確認ください。"
        link = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000164708_00001.html"
    if 'ワクチン' in search.search_query.query:
        message = "新型コロナワクチンに関する信頼できる情報をお求めの場合は、公的機関のページが役に立つでしょう。"
        link = "https://v-sys.mhlw.go.jp/"
    if 'サル痘' in search.search_query.query:
        message = "サル痘に関する情報をお求めの場合は、厚生労働省のwebサイトをご確認ください。"
        link = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou/kekkaku-kansenshou19/monkeypox_00001.html"
    if 'ウクライナ' in search.search_query.query:
        message = "ユニセフの緊急募金に参加しウクライナを支援できます。"
        link = "https://www.unicef.or.jp/kinkyu/ukraine/"
    
    if 'message' in locals():
        if 'link' in locals():
            search.result_container.answers['warning'] = {'answer': message, 'url': link}
        else:
            search.result_container.answers['warning'] = {'answer': message}
    
    return True
        
        