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
    println!("[INFO] Starting subsystem org.freasearch.intelligence-engine/weather...");
    thread::spawn(|| {
        start_server("bash", " /var/frea/subsystems/org.freasearch.intelligence-engine/init/weather.sh", 5);
    });

    println!("[INFO] Starting subsystem org.freasearch.intelligence-engine/train...");
    thread::spawn(|| {
        start_server("bash", "/var/frea/subsystems/org.freasearch.intelligence-engine/init/train.sh", 5);
    });

    println!("[INFO] Starting subsystem org.freasearch.intelligence-engine/tsunami...");
    thread::spawn(|| {
        start_server("bash", "/var/frea/subsystems/org.freasearch.intelligence-engine/init/tsunami.sh", 5);
    });

    println!("[INFO] Starting subsystem init_db...");
    thread::spawn(|| {
        start_server("python3", "/var/frea/subsystems/org.freasearch.innocence-force/init_db.py", 5);
    });

    println!("[INFO] Starting main server...");
    start_server("/usr/libexec/init-server.sh", "15", 3);
}