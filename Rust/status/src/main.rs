use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use time::{macros::date, OffsetDateTime, Duration};
use std::cmp::min;

fn main() {
    let path = Path::new("../README.md");
    let display = path.display();

    let mut file = match File::create(&path){
        Err(why) => panic!("Couldn't create {}: {}", display, why),
        Ok(file) => file,
    };

    let mut text = String::from("# Advent of Code 2022 - Rust 🦀\n\n");

    let startdate = date!(2022-11-30);
    let now = OffsetDateTime::now_utc();
    let today = now.date();

    if startdate >= today {
        let delta: Duration = startdate - today;
        let days = delta.whole_days() + 1;
        text.push_str(&format!("AoC hasn't started yet. It will start in {days} days!\n"))
    } else {
        text.push_str("AoC already started!\n\n");
        let delta: Duration = today - startdate;
        let days = min(delta.whole_days(), 25);
        let mut puzzles: u16 = 0;
        let mut complete_days: u16 = 0;
        for d in 1..(days+1) {
            text.push_str(&format!("* [Day {d:02}](day{d:02})"));
            let fname = &format!("../day{d:02}/status");
            let path_st = Path::new(fname);
            if path_st.exists() {
                let mut f = File::open(path_st).expect("The file couldn't be read");
                let mut s = String::new();
                f.read_to_string(&mut s).expect("The string couldn't be read");
                if s == String::from("2\n") {
                    text.push_str("🟩\n");
                    puzzles = puzzles + 2;
                    complete_days = complete_days + 1;
                } else if s == String::from("1\n") {
                    text.push_str("🟨\n");
                    puzzles = puzzles + 1;
                } else {
                    text.push_str("🟥\n");
                }
            } else {
                text.push_str("🟦\n");
            }
        }
        let tot_puzzles = 2 * days;
        let perc_puzzles: f32 = 50.0*(puzzles as f32)/(days as f32);
        let perc_days: f32 = 100.0*(complete_days as f32)/(days as f32);
        text.push_str(&format!("\nPuzzles completed: {puzzles}/{tot_puzzles} ({perc_puzzles:.2}%)"));
        text.push_str(&format!("\nDays completed: {complete_days}/{days} ({perc_days:.2}%)\n"));
    }

    match file.write_all(text.as_bytes()) {
        Err(why) => panic!("Couldn't write to {}: {}", display, why),
        Ok(_) => print!("Status updated!")
    };

}
