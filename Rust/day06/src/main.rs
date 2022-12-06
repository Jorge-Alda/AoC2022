use std::collections::HashSet;
use std::{error::Error, fmt};
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

#[derive(Debug, PartialEq)]
struct PositionError;

impl Error for PositionError {}

impl fmt::Display for PositionError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "We haven't found the position")
    }
}

fn position(input: String, len: usize) -> Result<usize, PositionError> {
    let characters: Vec<char> = input.chars().collect();
    for i in 0..input.len()-len {
        let slice = &characters[i..i+len];
        let set: HashSet<&char> = HashSet::from_iter(slice.iter());
        if set.len() == len{
            return Ok(i + len);
        }
    }
    Err(PositionError)
}

fn main() {
            
    let path_st = Path::new("status");

    let input = include_str!("../input").trim();
    let res = position(String::from(input), 4).unwrap();
    
    let path_o1 = Path::new("output1");
    let mut file = File::create(path_o1).unwrap();
    file.write_all(format!("{res}").as_bytes()).unwrap();

    let mut file = File::create(path_st).unwrap();
    file.write_all("1\n".as_bytes()).unwrap();
    
    let input = include_str!("../input").trim();
    let res = position(String::from(input), 14).unwrap();

    let path_o2 = Path::new("output2");
    let mut file = File::create(path_o2).unwrap();
    file.write_all(format!("{res}").as_bytes()).unwrap();

    let mut file = File::create(path_st).unwrap();
    file.write_all("2\n".as_bytes()).unwrap();
    
}


#[cfg(test)]
mod tests {
    #[test]
    fn test_part1(){
        assert_eq!(crate::position(String::from("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 4).unwrap(), 7);
        assert_eq!(crate::position(String::from("bvwbjplbgvbhsrlpgdmjqwftvncz"), 4).unwrap(), 5);
        assert_eq!(crate::position(String::from("nppdvjthqldpwncqszvftbrmjlhg"), 4).unwrap(), 6);
        assert_eq!(crate::position(String::from("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 4).unwrap(), 10);
        assert_eq!(crate::position(String::from("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 4).unwrap(), 11);
    }

    #[test]
    fn test_part2(){
        assert_eq!(crate::position(String::from("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 14).unwrap(), 19);
        assert_eq!(crate::position(String::from("bvwbjplbgvbhsrlpgdmjqwftvncz"), 14).unwrap(), 23);
        assert_eq!(crate::position(String::from("nppdvjthqldpwncqszvftbrmjlhg"), 14).unwrap(), 23);
        assert_eq!(crate::position(String::from("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 14).unwrap(), 29);
        assert_eq!(crate::position(String::from("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 14).unwrap(), 26);
    }
}