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

fn part2(input: String) -> i32 {
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
    let mut max1: i32 = 0;
    let mut max2: i32 = 0;
    let mut max3: i32 = 0;
    for c in elfs {
        if c > max1 {
            max3 = max2;
            max2 = max1;
            max1 = c;
        } else if c > max2 {
            max3 = max2;
            max2 = c;
        } else if c > max3 {
            max3 = c;
        }
    }
    return max1 + max2 + max3;
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

    println!("Part 2");
    let mut file_input = File::open(path_input).expect("The file couldn't be read");
    let mut inp = String::new();
    file_input.read_to_string(&mut inp).expect("The string couldn't be read");
    let out2 = part2(inp);
    println!("{}\n", out2);
    let mut file_st = File::create(&path_st).expect("Couldn't create the file");
    file_st.write_all("2\n".as_bytes()).expect("Couldn't write to file");
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
        assert_eq!(res, 24000);
    }

    #[test]
    fn part2(){
        let path_test = Path::new("test");
        let mut file_test = File::open(path_test).expect("The file couldn't be read");
        let mut s = String::new();
        file_test.read_to_string(&mut s).expect("The string couldn't be read");
        let res = crate::part2(s);
        assert_eq!(res, 45000);
    }
}