const cheerio = require("cheerio");
const axios = require("axios");
const http = require('http');
const url = require('url');

const AXIOS_OPTIONS = {
    headers: {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    },
};


const requestListener = function(req, res) {

    const queryObject = url.parse(req.url, true).query;
    const searchString = queryObject.q;
    const encodedString = encodeURI(searchString);

    function getResults() {
        return axios
            .get(
                `https://www.google.com/search?q=${encodedString}&hl=jp`,
                AXIOS_OPTIONS
            )
            .then(function({
                data
            }) {
                let $ = cheerio.load(data);

                const urls = [];
                const titles = [];
                const snippets = [];

                $(".yuRUbf > a").each((i, el) => {
                    urls[i] = $(el).attr("href");
                });
                $(".yuRUbf > a > h3").each((i, el) => {
                    titles[i] = $(el).text();
                });
                $(".IsZvec").each((i, el) => {
                    snippets[i] = $(el).text().trim();
                });

                const result = [];
                for (let i = 0; i < urls.length; i++) {
                    result[i] = {
                        url: urls[i],
                        title: titles[i],
                        snippet: snippets[i],
                    };
                }

                var resultJson = JSON.stringify(result);
                res.writeHead(200);
                res.end(resultJson);
            });
    }

    getResults();

}

const server = http.createServer(requestListener);
server.listen(8080);