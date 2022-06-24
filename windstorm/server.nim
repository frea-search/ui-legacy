import os
import std/asynchttpserver
import std/asyncdispatch
import std/httpclient
import urlly
import parsetoml
import std/json
import strutils

let debug_mode = true


proc msg_info(message: string) =
  echo "\e[32m✔ \e[m" & message

proc msg_err(message: string) =
  echo "\e[31m[✘ ERROR] \e[m" & message

proc emerg(message: string) =
  echo "\e[31m[✘ EMERG] \e[m" & message
  echo "\e[31mEXIT(1): We failed, but the fail whale is dead. Sorry....\e[m"
  quit(1)

proc msg_dbg(message: string) =
  if debug_mode == true:
    echo "\e[37m[DEBUG] " & message & "\e[m"


msg_info "starting FreaSearch server..."

if os.existsFile("kill.rules") == false:
  emerg "Kill.rules not found!!"

let kill_rules = parsetoml.parseFile("kill.rules")
let purge_domains = kill_rules["purge_domain"].getElems
let purge_domains_counts = purge_domains.len

var join_loop_counts = 0
var purge_domains_string:string

while join_loop_counts < purge_domains_counts:
  purge_domains_string.add ($purge_domains[join_loop_counts] & " ")
  join_loop_counts += 1

msg_dbg "Load " & $purge_domains_counts & " domains for purge."


proc main() {.async.} =
  var server = newAsyncHttpServer()
  
  proc cb(req: Request) {.async, gcsafe.} =
    msg_dbg "Received a request"    
    let path = $req.url.path

    if path == "/search":
      # 検索リクエストへの応答処理
      let headers = {"Content-type": "application/json; charset=utf-8"}
      let params = parseUrl("?" & $req.url.query)
      let keyword = $params.query["q"]

      # Googleクローラーにリクエストを送信し結果を取得
      msg_dbg "Sending a request to Google..."
      var client = newHttpClient()
      var google_result = try: parseJson(client.getContent("http://127.0.0.1:8080/?q=" & keyword))
                          except: %* {"error": getCurrentException().msg}
      
      if google_result.hasKey("error"):
        emerg "Failed to communicate with the google crawl service: " & google_result["error"].getStr & "\n\n<client>\e[32m OK\e[m\n↕\e[32m OK\e[m\n<server>\e[32m OK\e[m\n↕ \e[31mFAILD\e[m\n<google crawl service>\n\n >>>Is the google crawl service working?\n"

      # 結果の最適化
      msg_dbg "Start optimizing the results."
      var purge_loop_counts = 0

      while purge_loop_counts < google_result.len:

        var url_hostname = parseUrl(google_result[purge_loop_counts]["url"].getStr).hostname

        if url_hostname in purge_domains_string:
          google_result[purge_loop_counts]["purge"] = newJBool(true)
        else:
          google_result[purge_loop_counts]["purge"] = newJBool(false)

        purge_loop_counts += 1

      # リクエストへの応答
      msg_dbg "Done. Respond to the client."
      await req.respond(Http200, $google_result, headers.newHttpHeaders()) 
    else:
      # 不正なリクエストへの処理
      msg_err "Received an invalid request."
      let headers = {"Content-type": "text/plain; charset=utf-8"}
      await req.respond(Http400, "Bad Request :(", headers.newHttpHeaders())

  server.listen(Port(8081))
  msg_info "Server is ready!"

  while true:
    if server.shouldAcceptRequest():
      await server.acceptRequest(cb)
    else:
      await sleepAsync(500)

waitFor main()
