use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

fn priority(item: char) -> u32 {
    let p = item as u32;
    if p > 96 {
        p-96
    }else {
        p-38
    }
}

fn part1(input: String) -> u32 {
    let mut tot: u32 = 0;
    for rucksack in input.split('\n') {
        let l = rucksack.len()/2;
        let r1 = &rucksack[..l];
        let r2 = &rucksack[l..];
        for it1 in r1.chars() {
            if r2.contains(it1) {
                tot = tot + priority(it1);
                break;
            }
        }
    }
    tot
}

fn part2(input: String) -> u32 {
    let mut tot: u32 = 0;
    let rucksacks: Vec<&str> = input.split('\n').collect();
    for i in 0..rucksacks.len()/3 {
        let r1 = rucksacks[3*i];
        let r2 = rucksacks[3*i+1];
        let r3 = rucksacks[3*i+2];
        for item in r1.chars() {
            if r2.contains(item) & r3.contains(item){
                tot = tot + priority(item);
                break;
            }
        }
    }
    tot
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
    fn test_priority(){
        let c1 = 'p';
        let res1 = crate::priority(c1);
        assert_eq!(res1, 16);
        let c2 = 'L';
        let res2 = crate::priority(c2);
        assert_eq!(res2, 38);
    }


    #[test]
    fn test_part1(){
        let input = include_str!("../test");
        let res = crate::part1(String::from(input.trim()));
        assert_eq!(res, 157);
    }

    #[test]
    fn test_part2(){
        let input = include_str!("../test");
        let res = crate::part2(String::from(input.trim()));
        assert_eq!(res, 70);
    }
}