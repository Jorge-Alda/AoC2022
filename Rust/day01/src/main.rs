use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use std::str::FromStr;

fn part1(input: String) -> i32 {
    let mut elfs: Vec<i32> = Vec::new();
    let mut calories: i32 = 0;
    for l in input.split('\n') {
        if l == "" {
            elfs.push(calories);
            calories = 0;
        } else {
            let newcal: i32 = FromStr::from_str(l).unwrap();
            calories = calories + newcal;
        }
    }
    elfs.push(calories);
    let mut max:i32 = 0;
    for c in elfs {
        if c > max {
            max = c;
        }
    }
    return max;
}

fn main() {
    println!("Starting");
    let path_st = Path::new("status");

    let mut file_st = File::create(&path_st).expect("Couldn't create the file");
    file_st.write_all("0\n".as_bytes()).expect("Couldn't write to file");

    println!("Part 1");
    let path_input = Path::new("input");
    let mut file_input = File::open(path_input).expect("The file couldn't be read");
    let mut inp = String::new();
    file_input.read_to_string(&mut inp).expect("The string couldn't be read");
    let out1 = part1(inp);
    println!("{}\n", out1);
    let mut file_st = File::create(&path_st).expect("Couldn't create the file");
    file_st.write_all("1\n".as_bytes()).expect("Couldn't write to file");
}

#[cfg(test)]
mod tests {
    use std::path::Path;
    use std::io::prelude::*;
    use std::fs::File;

    #[test]
    fn part1(){
        let path_test = Path::new("test");
        let mut file_test = File::open(path_test).expect("The file couldn't be read");
        let mut s = String::new();
        file_test.read_to_string(&mut s).expect("The string couldn't be read");
        let res = crate::part1(s);
        assert_eq!(res, 24000)
    }
}