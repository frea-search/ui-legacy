extern crate postgres;
use std::env;
use std::process::exit;
use postgres::{Client, Error, NoTls};

fn main() -> Result<(), Error> {
    let args: Vec<String> = env::args().collect();
    let mut client = Client::connect(
        "postgresql://freasearch:freasearch@db:5432/freasearch",
        NoTls,
    )?;

    let command: String = "SELECT url FROM blocklist WHERE url='".to_owned() +  &args[1] + "'";

    for row in client.query(&command, &[])? {
        let url: String = row.get(0);
        if ! url.is_empty() {
            println!("1");
            exit(0);
        }
    }

    println!("0");
    exit(0);
}