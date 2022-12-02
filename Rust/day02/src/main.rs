use std::collections::HashMap;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

enum GameResults {
    Win,
    Draw,
    Lose
}

impl GameResults {
    fn score(&self) -> u32 {
        match self {
            &GameResults::Lose => 0,
            &GameResults::Draw => 3,
            &GameResults::Win => 6,
        }
    }
}

enum RockPaperScissors{
    Rock,
    Paper,
    Scissors,
}

impl RockPaperScissors{
    fn value(&self) -> i8 {
        match self {
            &RockPaperScissors::Rock => 1,
            &RockPaperScissors::Paper => 2,
            &RockPaperScissors::Scissors => 3,
        }
    }

    fn result(&self, rival: &RockPaperScissors) -> GameResults {
        let r= self.value()-rival.value();
        match r {
            0 => GameResults::Draw,
            1 => GameResults::Win,
            -2 => GameResults::Win,
            _ => GameResults::Lose,
        }
    }

    fn score(&self, rival: &RockPaperScissors) -> u32 {
        let s = self.result(rival).score();
        (self.value() as u32) + s
    }

    fn rig_game(&self, result: &GameResults) -> &RockPaperScissors {
        match result {
            &GameResults::Draw => self,
            &GameResults::Win => {
                match self {
                    &RockPaperScissors::Rock => &RockPaperScissors::Paper,
                    &RockPaperScissors::Paper => &RockPaperScissors::Scissors,
                    &RockPaperScissors::Scissors => &RockPaperScissors::Rock,
                }},
            &GameResults::Lose => {
                match self {
                    &RockPaperScissors::Rock => &RockPaperScissors::Scissors,
                    &RockPaperScissors::Paper => &RockPaperScissors::Rock,
                    &RockPaperScissors::Scissors => &RockPaperScissors::Paper,
                }
            },
        }
    }
}

fn part1(input: String) -> u32 {
    let mut tot: u32 = 0;
    let elf_code = HashMap::from([('A', RockPaperScissors::Rock), ('B', RockPaperScissors::Paper), ('C', RockPaperScissors::Scissors)]);
    let human_code = HashMap::from([('X', RockPaperScissors::Rock), ('Y', RockPaperScissors::Paper), ('Z', RockPaperScissors::Scissors)]);
    for game in input.split('\n') {
        let e = game.chars().nth(0).unwrap();
        let h = game.chars().nth(2).unwrap();
        let e_play = elf_code.get(&e).unwrap();
        let h_play = human_code.get(&h).unwrap();
        tot = tot + h_play.score(e_play);
    }
    tot
}

fn part2(input: String) -> u32 {
    let mut tot: u32 = 0;
    let elf_code = HashMap::from([('A', RockPaperScissors::Rock), ('B', RockPaperScissors::Paper), ('C', RockPaperScissors::Scissors)]);
    let results_code = HashMap::from([('X', GameResults::Lose), ('Y', GameResults::Draw), ('Z', GameResults::Win)]);
    for game in input.split('\n') {
        let e = game.chars().nth(0).unwrap();
        let h = game.chars().nth(2).unwrap();
        let e_play = elf_code.get(&e).unwrap();
        let res = results_code.get(&h).unwrap();
        let h_play = e_play.rig_game(res);
        tot = tot + h_play.score(e_play);
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
    fn test_part1(){
        let input = include_str!("../test");
        let res = crate::part1(String::from(input.trim()));
        assert_eq!(res, 15);
    }

    #[test]
    fn test_part2(){
        let input = include_str!("../test");
        let res = crate::part2(String::from(input.trim()));
        assert_eq!(res, 12);
    }
}