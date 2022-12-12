use std::path;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

use itertools::Itertools;

fn parse(input: &str) -> (Vec<Vec<u8>>, (usize, usize), (usize, usize)) {
    let lines = input.split('\n').collect::<Vec<&str>>();
    let lenx = lines.len();
    let leny = lines[0].len();
    let mut sx: usize = 0;
    let mut sy: usize = 0;
    let mut ex: usize = 0;
    let mut ey: usize = 0;
    let mut hmap = vec![vec![0_u8; leny]; lenx];

    for (x, &l) in lines.iter().enumerate() {
        for (y, c) in l.chars().enumerate() {
            if c == 'S' {
                sx = x;
                sy = y;
                hmap[x][y] = 0;
            } else if c == 'E' {
                ex = x;
                ey = y;
                hmap[x][y] = ('z' as u8) - ('a' as u8);
            } else {
                hmap[x][y] = (c as u8) - ('a' as u8);
            }
        }
    }

    (hmap, (sx, sy), (ex, ey))
}


fn shortest_path (hmap: &Vec<Vec<u8>>, start: (usize, usize), end: (usize, usize)) -> Result<i32, ()> {
    let lenx = hmap.len();
    let leny = hmap[0].len();
    let mut candidates = vec![start];
    let mut visited = vec![start];
    let mut steps: i32 = 0;
    let mut stop = false;
    while !stop {
        if candidates.len() == 0 {
            return  Err(());
        }
        let mut new: Vec<(usize, usize)> = Vec::new();
        for p in &candidates {
            let mut neighbours: Vec<(usize, usize)>= Vec::new();
            if p.0 > 0 {
                neighbours.push((p.0-1, p.1));
            } 
            if p.0 < lenx-1 {
                neighbours.push((p.0+1, p.1));
            }
            if p.1 > 0 {
                neighbours.push((p.0, p.1-1));
            }
            if p.1 < leny-1 {
                neighbours.push((p.0, p.1+1));
            }
            for np in neighbours {
                if !(visited.contains(&np)) & ((hmap[np.0][np.1] as i16) - (hmap[p.0][p.1] as i16) <= 1) {
                    if np == end {
                        stop = true;
                    }
                    new.push(np);
                    visited.push(np);
                } 
            }
        }
        steps += 1;
        candidates = new;
    }

    Ok(steps)
}


fn part1(input: &str) -> i32 {
    let (hmap, start, end) = parse(input);
    shortest_path(&hmap, start, end).unwrap()
}


fn part2(input: &str) -> i32 {
    let (hmap, _, end) = parse(input);
    let lenx = hmap.len();
    let leny = hmap[0].len();
    let starts = (0..lenx).cartesian_product(0..leny)
        .filter(|(x, y)| hmap[*x][*y] == 0)
        .collect::<Vec<(usize, usize)>>();
    let mut paths: Vec<i32> = Vec::new();
    for s in starts {
        match shortest_path(&hmap, s, end) {
            Ok(p) => {paths.push(p);},
            _ => {},
        }
    }
    *paths.iter().min().unwrap()
}

fn main() {
        
    let path_st = Path::new("status");

    let input = include_str!("../input").trim();
    let res_1 = part1(input);
    let res_2 = part2(input);
    
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
        let res = crate::part1(input);
        assert_eq!(res, 31);
    }

    #[test]
    fn test_part2(){
        let input = include_str!("../test").trim();
        let res = crate::part2(input);
        assert_eq!(res, 29);
    }
}