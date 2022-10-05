use std::thread;
use std::process::Command;
use std::process::exit;


fn start_server(cmd: &str, arg: &str, restart_limit: i32) {

    println!("[INFO] Start server: {}", cmd);
    let mut restart_counts = 0;

    loop {
        let args = arg.split_whitespace();

        let status = Command::new(cmd)
                                                       .args(args)
                                                       .status()
                                                       .expect("[FETAL] Failed to execute command. init will abort with SIGABRT!!!!");

        if status.success() {
            println!("[INFO] Command {} exited with code 0", cmd);
            break();
        } else {
            eprintln!("[ERROR] Command {} exited with code != 0", cmd);
            restart_counts += 1;
        }

        if  restart_limit < restart_counts {
            eprintln!("[FETAL] restart_limit exceeded. Exit :(");
            exit(1);
        }

    }
    
}

fn main() {

    thread::spawn(|| {
        start_server("ls", "./", 5);
    });

    println!("Starting main server...");
    start_server("sleep", "15", 3);
}