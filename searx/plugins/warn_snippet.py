name = "Warning snippet"
description = "Displays advice and warnings."
default_on = True

def post_search(request, search):
    if search.search_query.pageno > 1:
        return True
    if 'コロナ' in search.search_query.query:
        message = "新型コロナウイルス感染症に関する正しい情報をお求めの場合は、<a href=\"https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000164708_00001.html\">厚生労働省のwebサイト</a>をご確認ください。"
    if 'ワクチン' in search.search_query.query:
        message = "新型コロナワクチンに関する信頼できる情報をお求めの場合は、<a href=\"https://v-sys.mhlw.go.jp/\">公的機関のページ</a>が役に立つでしょう。"
    if 'ウクライナ' in search.search_query.query:
        message = "<a href=\"https://www.unicef.or.jp/kinkyu/ukraine/\">ユニセフの緊急募金</a>に参加しウクライナを支援できます。"
    search.result_container.answers['warning'] = {'answer': message}
    return True