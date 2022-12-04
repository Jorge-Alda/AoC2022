use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

fn part1(input: String) -> u16 {
    let mut overlaps: u16 = 0;
    for l in input.split('\n') {
        let elfs: Vec<&str> = l.split(',').collect();
        let elf1: Vec<&str> = elfs[0].split('-').collect();
        let elf2: Vec<&str> = elfs[1].split('-').collect();
        let start1: u32 = elf1[0].parse().unwrap();
        let end1: u32 = elf1[1].parse().unwrap();
        let start2: u32 = elf2[0].parse().unwrap();
        let end2: u32 = elf2[1].parse().unwrap();
        if (start1 <= start2) & (end1 >= end2) {
            overlaps = overlaps +1;
        } else if (start1 >= start2) & (end1 <= end2){
            overlaps = overlaps +1;
        }
    }
    overlaps
}

fn part2(input: String) -> u16 {
    let mut overlaps: u16 = 0;
    for l in input.split('\n') {
        let elfs: Vec<&str> = l.split(',').collect();
        let elf1: Vec<&str> = elfs[0].split('-').collect();
        let elf2: Vec<&str> = elfs[1].split('-').collect();
        let start1: u32 = elf1[0].parse().unwrap();
        let end1: u32 = elf1[1].parse().unwrap();
        let start2: u32 = elf2[0].parse().unwrap();
        let end2: u32 = elf2[1].parse().unwrap();
        if (end1 >= start2) & (end2 >= start1){
            overlaps = overlaps + 1;
        }
    }
    overlaps
}

fn main() {
    
    let path_st = Path::new("status");

    let input = include_str!("../input");
    let res = crate::part1(String::from(input.trim()));
    
    let path_o1 = Path::new("output1");
    let mut file = File::create(path_o1).unwrap();
    file.write_all(format!("{res}").as_bytes()).unwrap();

    let mut file = File::create(path_st).unwrap();
    file.write_all("1\n".as_bytes()).unwrap();


    let input = include_str!("../input");
    let res = crate::part2(String::from(input.trim()));
    
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
        let input = include_str!("../test");
        let res = crate::part1(String::from(input.trim()));
        assert_eq!(res, 2);
    }

    #[test]
    fn test_part2(){
        let input = include_str!("../test");
        let res = crate::part2(String::from(input.trim()));
        assert_eq!(res, 4);
    }
}