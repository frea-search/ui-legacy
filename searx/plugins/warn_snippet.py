name = "Warning snippet"
description = "Displays advice and warnings."
default_on = True

def post_search(request, search):
    if search.search_query.pageno > 1:
        return True
    if 'コロナ' in search.search_query.query:
        message = "新型コロナウイルス感染症に関する正しい情報をお求めの場合は、厚生労働省のwebサイト(https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000164708_00001.html)をご確認ください。"
    if 'ワクチン' in search.search_query.query:
        message = "新型コロナワクチンに関する信頼できる情報をお求めの場合は、公的機関のページ(https://v-sys.mhlw.go.jp/)が役に立つでしょう。"
    if 'サル痘' in search.search_query.query:
        message = "サル痘に関する情報をお求めの場合は、厚生労働省のwebサイト(https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou/kekkaku-kansenshou19/monkeypox_00001.html)をご確認ください。"
    if 'ウクライナ' in search.search_query.query:
        message = "ユニセフの緊急募金(https://www.unicef.or.jp/kinkyu/ukraine/)に参加しウクライナを支援できます。"
    
    if len(message) == 0:
        return True
    else:
        search.result_container.answers['warning'] = {'answer': message}
        return True