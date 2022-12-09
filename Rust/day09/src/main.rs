use std::collections::HashSet;
use std::convert::From;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;


#[derive(Debug,PartialEq,Eq,Clone)]
enum Movement {
    Up,
    Down,
    Right,
    Left,
}


impl From<char> for Movement {
    fn from(dir: char) -> Self {
        match dir {
            'U' => Movement::Up,
            'D' => Movement::Down,
            'R' => Movement::Right,
            _ => Movement::Left,
        }
    }
}

struct Rope {
    n_knots: usize,
    coords: Vec<(i32, i32)>,
}

impl Rope {
    fn new(knots: usize) -> Self {
        Rope { n_knots: knots, coords: vec![(0, 0); knots+1] }
    }

    fn move_rope(&mut self, m: Movement) {
        self.coords[0] = move_knot(m, self.coords[0]);

        for k in 1..(self.n_knots+1) {
            let rel_x = self.coords[k-1].0 - self.coords[k].0;
            let rel_y = self.coords[k-1].1 - self.coords[k].1;
            if rel_x.pow(2) + rel_y.pow(2) > 2 {
                let x = self.coords[k].0 + delta(rel_x);
                let y = self.coords[k].1 + delta(rel_y);
                self.coords[k] = (x, y);
            }
        }
    }
}

fn delta(x: i32) -> i32 {
    if x > 0 {
        1
    } else if x == 0 {
        0
    } else {
        -1
    }
}

fn parse(input: String) -> Vec<Movement> {
    let mut moves: Vec<Movement> = Vec::new();
    for l in input.split('\n') {
        let dir = l.chars().nth(0).unwrap();
        let m = Movement::from(dir);
        let num = l.chars()
            .skip(2)
            .collect::<String>()
            .parse::<usize>()
            .unwrap();
        moves.append(&mut vec![m;num]);
    }

    moves
}

fn move_knot(m: Movement, pos: (i32, i32)) -> (i32, i32){
    match m {
        Movement::Up => (pos.0, pos.1+1),
        Movement::Down => (pos.0, pos.1-1),
        Movement::Right => (pos.0+1, pos.1),
        Movement::Left => (pos.0-1, pos.1),
    }
}

fn solve(input: String) -> (usize, usize){
    let mut positions_p1 = HashSet::new();
    let mut positions_p2 = HashSet::new();
    let mut rope = Rope::new(9);
    for m in parse(input) {
        rope.move_rope(m);
        positions_p1.insert(rope.coords[1]);
        positions_p2.insert(rope.coords[9]);
    }
    (positions_p1.len(), positions_p2.len())
}

fn main() {
        
    let path_st = Path::new("status");

    let input = include_str!("../input").trim();
    let res = solve(String::from(input));
    let res_1 = res.0;
    let res_2 = res.1;
    
    let path_o1 = Path::new("output1");
    let mut file = File::create(path_o1).unwrap();
    file.write_all(format!("{res_1}").as_bytes()).unwrap();

    let mut file = File::create(path_st).unwrap();
    file.write_all("1\n".as_bytes()).unwrap();
    
    let path_o2 = Path::new("output2");
    let mut file = File::create(path_o2).unwrap();
    file.write_all(format!("{res_2}").as_bytes()).unwrap();

    let mut file = File::create(path_st).unwrap();
    file.write_all("2\n".as_bytes()).unwrap();

}


#[cfg(test)]
mod test {
    #[test]
    fn test_part1(){
        let input = include_str!("../test").trim();
        let res = crate::solve(String::from(input)).0;
        assert_eq!(res, 13);
    }
}