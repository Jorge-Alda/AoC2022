use std::collections::BinaryHeap;
use std::ops::Add;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

#[derive(Debug, PartialEq, Eq, Clone, Copy, Hash)]
struct Point {
    x: i32,
    y: i32,
}


impl Add for Point {
    type Output = Point;
    fn add(self, rhs: Self) -> Self::Output {
        Point { x: self.x + rhs.x, y: self.y + rhs.y }
    }
}

impl TryFrom<&str> for Point {
    type Error = ();
    fn try_from(value: &str) -> Result<Self, Self::Error> {
        let v = value.split(',').collect::<Vec<&str>>();
        if v.len() != 2 {
            return Err(());
        }
        let vx = v[0].parse::<i32>();
        let vy = v[1].parse::<i32>();
        match (vx, vy) {
            (Ok(x), Ok(y)) => Ok(Point { x, y }),
            _ => Err(()),
        }
    }
}


fn parse_rocks(input: &str) -> Vec<Point>{
    let mut rocks: Vec<Point> = Vec::new();
    for l in input.lines() {
        let points = l.split(" -> ")
            .map(|p| Point::try_from(p).unwrap())
            .collect::<Vec<Point>>();
        for i in 1..points.len() {
            if points[i].x != points[i-1].x {
                let mut bheap = BinaryHeap::from(vec![points[i].x, points[i-1].x]);
                let maxx = bheap.pop().unwrap();
                let minx = bheap.pop().unwrap();
                for x in minx..=maxx {
                    rocks.push(Point {x, y: points[i].y});
                }
            } else {
                let mut bheap = BinaryHeap::from(vec![points[i].y, points[i-1].y]);
                let maxy = bheap.pop().unwrap();
                let miny = bheap.pop().unwrap();
                for y in miny..=maxy {
                    rocks.push(Point {x: points[i].x, y});
                }                
            }
        }
    }
    
    rocks
}


fn solve(rocks: Vec<Point>) -> (u32, u32){
    let mut sand: u32 = 0;
    let mut cave = rocks.clone();
    let mut part1: u32 = 0;
    let floor = rocks.iter().map(|p| p.y).max().unwrap();
    let nextpos = [Point {x: 0, y: 1}, Point {x: -1, y: 1}, Point {x: 1, y: 1}];
    loop {
        let mut pos = Point {x: 500, y: 0};
            loop {
                if pos.y == floor+1 {
                    if part1 == 0 {
                        part1 = sand;
                    }
                    cave.push(pos);
                    break;
                }
                let drops = nextpos.map(|p| pos + p);
                let nextdrop = drops.iter().filter(|&p| !cave.contains(p))
                    .collect::<Vec<&Point>>();
                if nextdrop.is_empty() {
                    cave.push(pos);
                    break;
                } else {
                    pos = Point {x: nextdrop[0].x, y: nextdrop[0].y };
                }
                
            }
        sand += 1;
        if cave.last().unwrap().y == 0 {
            break;
        }
    }
    (part1, sand)
}

fn main() {
    let path_st = Path::new("status");
    
    let input = include_str!("../input").trim();
    let rocks = parse_rocks(input);
    let (res_1, res_2) = solve(rocks);
    
    
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
    use crate::{solve, parse_rocks};

    #[test]
    fn test_solution(){
        let input = include_str!("../test").trim();
        let rocks = parse_rocks(input);
        let res = solve(rocks);
        assert_eq!(res.0, 24);
        assert_eq!(res.1, 93);
    }
}