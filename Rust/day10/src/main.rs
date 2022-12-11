use itertools;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

mod ocr;

pub use crate::ocr::ocr_scan;

fn solve(input: String) -> (i32, String) {
    let mut screen = String::new();
    let mut commands = input.split('\n')
        .rev()
        .collect::<Vec<&str>>();
    let mut waiting = false;
    let mut strengths: i32 = 0;
    let mut X: i32 = 1;
    let mut command = "";
    let mut target_cycle: usize = 19;
    for cycle in 0..240usize {
        if (((cycle % 40) as i32) - X).abs() <= 1 {
            screen.push('#');
        } else {
            screen.push('.');
        }
        if cycle % 40 == 39 {
            screen.push('\n');
        }
        if cycle == target_cycle {
            strengths += X * (cycle as i32 + 1);
            target_cycle += 40;
        }
        if waiting {
            waiting = false;
            X += command.strip_prefix("addx ")
                .unwrap()
                .parse::<i32>()
                .unwrap();
        } else {
            command = commands.pop().unwrap();
            if command.starts_with("addx ") {
                waiting = true;
            }
        }
    }
    (strengths, screen)
}

fn main() {
        
    let path_st = Path::new("status");

    let input = include_str!("../input").trim();
    let res = solve(String::from(input));
    let res_1 = res.0;
    let res_2 = res.1.trim().replace(".", " ");
    let res_2_ocr = ocr_scan(String::from(res_2)).unwrap();
    
    let path_o1 = Path::new("output1");
    let mut file = File::create(path_o1).unwrap();
    file.write_all(format!("{res_1}").as_bytes()).unwrap();

    let mut file = File::create(path_st).unwrap();
    file.write_all("1\n".as_bytes()).unwrap();
    
    let path_o2 = Path::new("output2");
    let mut file = File::create(path_o2).unwrap();
    file.write_all(format!("{res_2_ocr}").as_bytes()).unwrap();

    let mut file = File::create(path_st).unwrap();
    file.write_all("2\n".as_bytes()).unwrap();    

}

#[cfg(test)]
mod tests {
    #[test]
    fn test_part1(){
        let input = include_str!("../test").trim();
        let res = crate::solve(String::from(input)).0;
        assert_eq!(res, 13140);
    }

    #[test]
    fn test_part2(){
        let screen = "##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
";
        let input = include_str!("../test").trim();
        let res = crate::solve(String::from(input)).1;
        assert_eq!(&res, screen);
    }
}