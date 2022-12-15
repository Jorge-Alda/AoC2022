use std::ops::{BitAnd, BitOr};
use std::cmp::{PartialOrd, Ord, Ordering};
use std::fmt::Display;
use std::iter::zip;
use regex::Regex;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Extreme {
    Start,
    End,
    IStart,
    IEnd,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct Point {
    x: i32,
    ext: Extreme,
}

impl PartialOrd for Point {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        if self.x < other.x {
            Some(Ordering::Less)
        } else if self.x > other.x {
            Some(Ordering::Greater)
        } else if self.ext == Extreme::End {
            Some(Ordering::Greater)
        } else if other.ext == Extreme::End {
            Some(Ordering::Less)
        } else {
            Some(Ordering::Equal)
        }
    }
}

impl Ord for Point {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}


#[derive(Debug, Clone, PartialEq, Eq)]
struct Interval {
    endpoints: Vec<Point>
}

impl Interval {
    fn new(start: i32, end: i32) -> Self {
        if end > start {
            Interval {endpoints: vec![Point {x: start, ext: Extreme::Start}, Point {x: end, ext: Extreme::End}]}
        } else {
            Interval {endpoints: vec![Point {x: end, ext: Extreme::Start}, Point {x: start, ext: Extreme::End}]}
        }
    }

    fn length(self) -> u32 {
        let mut l: u32 = 0;
        for i in 0..(self.endpoints.len()/2) {
            l += (self.endpoints[2*i+1].x - self.endpoints[2*i].x + 1) as u32;
        }
        l
    }
}

impl Display for Interval {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let a = self.endpoints
            .chunks(2)
            .map(|p| format!("[{}, {}]", p[0].x, p[1].x))
            .collect::<Vec<String>>()
            .join(", ");
        write!(f, "{}", a)
    }
}

impl BitOr for Interval {
    type Output = Interval;
    fn bitor(self, rhs: Self) -> Self::Output {
        let mut res: Vec<Point> = Vec::new();
        if self.endpoints.is_empty() {
            res = rhs.endpoints;
        } else {
            let mut combined = self.endpoints.clone();
            combined.append(&mut rhs.endpoints.clone());
            combined.sort();
            let mut s = 0;
            let mut start_val = 0;
            let mut new_points: Vec<Point> = Vec::new();
            for p in combined {
                if s==0 && p.ext == Extreme::Start {
                    start_val = p.x;
                    s += 1;
                } else if s==1 && p.ext == Extreme::End {
                    new_points.push(Point {x: start_val, ext: Extreme::Start});
                    new_points.push(Point {x: p.x, ext: Extreme::End});
                    s = 0;
                } else if  p.ext == Extreme::Start {
                    s += 1;
                } else {
                    s -= 1;
                }
            }
            res.push(new_points[0]);
            for i in 0..(new_points.len()/2-1) {
                if new_points[2*i+1].x + 1 != new_points[2*i+2].x {
                    res.push(new_points[2*i+1]);
                    res.push(new_points[2*i+2]);
                }
            }
            res.push(*new_points.last().unwrap());
        }
        Interval {endpoints: res}
    }
}


impl BitAnd for Interval {
    type Output = Interval;
    fn bitand(self, rhs: Self) -> Self::Output {
        if self.endpoints.is_empty() || rhs.endpoints.is_empty() {
            Interval {endpoints: vec![]}
        } else if rhs.endpoints.len() > 2 {
            let mut res = Interval {endpoints: vec![]};
            for i in 0..(rhs.endpoints.len()/2) {
                let inter = self.clone() & Interval::new(rhs.endpoints[2*i].x, rhs.endpoints[2*i+1].x);
                res = res | inter;
            }
            res
        } else{
            let mut combined = self.endpoints.clone();
            combined.push(Point {x: rhs.endpoints[0].x, ext: Extreme::IStart});
            combined.push(Point {x: rhs.endpoints[1].x, ext: Extreme::IEnd});
            combined.sort();
            let mut s_i = false;
            let mut res = Interval {endpoints: vec![]};
            for (i, p) in combined.iter().enumerate() {
                if p.ext == Extreme::IStart{
                    s_i = true;
                    if (combined[i+1].ext == Extreme::IEnd) && (combined[i-1].ext == Extreme::End){
                        return res;
                    } else if (combined[i+1].ext == Extreme::IEnd) && (combined[i-1].ext == Extreme::Start) {
                        return rhs;
                    } else if combined[i+1].ext == Extreme::End {
                        res.endpoints.push(Point {x: p.x, ext: Extreme::Start});
                    }
                } else if p.ext == Extreme::IEnd {
                    if combined[i-1].ext == Extreme::Start {
                        res.endpoints.push(Point {x: p.x, ext: Extreme::End});
                    }
                    return res;
                } else if s_i {
                    res.endpoints.push(*p);
                }
            }
            res
        }
    }
}

fn parse_line(l: &str) -> ((i32, i32), (i32, i32)) {
    let exp = r"Sensor at x=(-?[0-9]*), y=(-?[0-9]*): closest beacon is at x=(-?[0-9]*), y=(-?[0-9]*)";
    let re = Regex::new(exp).unwrap();
    let captured = re.captures(l).unwrap();
    let x1 = captured.get(1).unwrap().as_str().parse::<i32>().unwrap();
    let y1 = captured.get(2).unwrap().as_str().parse::<i32>().unwrap();
    let x2 = captured.get(3).unwrap().as_str().parse::<i32>().unwrap();
    let y2 = captured.get(4).unwrap().as_str().parse::<i32>().unwrap();
    ((x1, y1), (x2, y2))
}

#[inline]
fn dist(p1: &(i32, i32), p2: &(i32, i32)) -> i32{
    (p1.0-p2.0).abs() + (p1.1-p2.1).abs()
}


fn covered_sensor(sensor: &(i32, i32), beacon: &(i32, i32), target: i32) -> Interval{
    let d = dist(sensor, beacon);
    let d_target = dist(sensor, &(sensor.0, target));
    if d_target > d {
        Interval {endpoints: vec![]}
    } else {
        Interval::new(sensor.0-(d-d_target), sensor.0+(d-d_target))
    }
}


fn scan(sensors: &Vec<(i32, i32)>, beacons: &Vec<(i32, i32)>, target: i32) -> Interval {
    let mut covered = Interval {endpoints: vec![]};
    for (sensor, beacon) in zip(sensors, beacons) {
        covered = covered | covered_sensor(sensor, beacon, target); 
    }
    covered
}


fn part1(input: &str, target: i32) -> u32 {
    let mut sensors: Vec<(i32, i32)> = Vec::new();
    let mut beacons: Vec<(i32, i32)> = Vec::new();
    for l in input.lines() {
        let (sensor, beacon) = parse_line(l);
        sensors.push(sensor);
        beacons.push(beacon);
    }
    scan(&sensors, &beacons, target).length() - 1
}


fn part2(input: &str, dim: i32) -> u64 {
    let mut sensors: Vec<(i32, i32)> = Vec::new();
    let mut beacons: Vec<(i32, i32)> = Vec::new();
    for l in input.lines() {
        let (sensor, beacon) = parse_line(l);
        sensors.push(sensor);
        beacons.push(beacon);
    }
    for y in 0..=dim {
        let covered = scan(&sensors, &beacons, y);
        let clipped = covered & Interval::new(0, dim);
        if clipped.endpoints.len() == 4 {
            let x = clipped.endpoints[1].x + 1;
            return 4_000_000*(x as u64) + (y as u64);
        }
    }
    0
}

fn main() {
    let path_st = Path::new("status");

    let input = include_str!("../input").trim();
    let res_1 = part1(input, 2000000);
    let res_2 = part2(input, 4_000_000);
    
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
    use crate::{Interval, part1, part2};
    #[test]
    fn test_part1(){
        let input = include_str!("../test").trim();
        let res = part1(input, 10);
        assert_eq!(res, 26);
    }

    #[test]
    fn test_part2(){
        let input = include_str!("../test").trim();
        let res = part2(input, 20);
        assert_eq!(res, 56000011);
    }

    #[test]
    fn union_disjoint() {
        let i1 = Interval::new(1, 7);
        let i2 = Interval::new(10, 13);
        let ires = i1 | i2;
        assert_eq!(format!("{}", ires), "[1, 7], [10, 13]");
    }

    #[test]
    fn union_overlap() {
        let i1 = Interval::new(9, 11);
        let i2 = Interval::new(10, 13);
        let ires = i1 | i2;
        assert_eq!(ires, Interval::new(9, 13));
    }

    #[test]
    fn union_multiple() {
        let i1 = Interval::new(1, 3) | Interval::new(11, 13);
        let i2 = Interval::new(2, 7) | Interval::new(9, 13);
        let itot = i1 | i2;
        assert_eq!(format!("{}", itot), "[1, 7], [9, 13]");
    }

    #[test]
    fn union_coincidence() {
        let i1 = Interval::new(1, 2) | Interval::new(2, 3);
        let i2 = Interval::new(1, 3);
        assert_eq!(i1, i2);
    }

    #[test]
    fn union_merge() {
        let i1 = Interval::new(1, 2) | Interval::new(3, 4);
        let i2 = Interval::new(1, 4);
        assert_eq!(i1, i2);
    }

    #[test]
    fn inter_contained() {
        let i1 = Interval::new(1, 10) & Interval::new(4, 5);
        let i2 = Interval::new(4, 5);
        assert_eq!(i1, i2);
    }

    #[test]
    fn inter_overlap() {
        let i1 = Interval::new(1, 10) & Interval::new(7, 13);
        let i2 = Interval::new(7, 10);
        assert_eq!(i1, i2);
    }

    #[test]
    fn inter_coincidence() {
        let i1 = Interval::new(1, 10) & Interval::new(7, 10);
        let i2 = Interval::new(7, 10);
        assert_eq!(i1, i2);
    }

    #[test]
    fn inter_union() {
        let i1 = Interval::new(1, 5) | Interval::new(8, 11);
        let i2 = i1 & Interval::new(3, 10);
        let i3 = Interval::new(3, 5) | Interval::new(8, 10);
        assert_eq!(i2, i3);
    }

    #[test]
    fn inter_mulunion() {
        let i1 = Interval::new(1, 5) | Interval::new(8, 15);
        let i2 = Interval::new(3, 10) | Interval::new(13, 21);
        let ires = i1 & i2;
        let i3 = Interval::new(3, 5) | Interval::new(8, 10) | Interval::new(13, 15);
        assert_eq!(ires, i3);
    }
}