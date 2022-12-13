use serde_json::Value;
use std::iter::zip;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use std::cmp::Ordering;

#[derive(Debug, PartialEq, Eq, Clone)]
enum Package {
    Number(u64),
    Packages(Vec<Package>),
}

impl TryFrom<&Value> for Package {
    type Error = ();
    fn try_from(value: &Value) -> Result<Self, Self::Error> {
        match value {
            Value::Number(n) => Ok(Self::Number(n.as_u64().unwrap())),
            Value::Array(a) => {
                let b = a.iter().map(|v| Package::try_from(v).unwrap() ).collect::<Vec<Package>>();
                Ok(Self::Packages(b))
            },
            _ => Err(()),
        }
    }
}

impl PartialOrd for Package {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        match (self, other) {
            (Package::Number(l), Package::Number(r)) => {
                if l < r {
                    Some(Ordering::Less)
                } else if l == r {
                    Some(Ordering::Equal)
                } else {
                    Some(Ordering::Greater)
                }
            },
            (Package::Number(l), Package::Packages(r)) => {
                Package::Packages(vec![Package::Number(l.to_owned())]).partial_cmp(&Package::Packages(r.to_vec()))
            },
            (Package::Packages(l), Package::Number(r)) => {
                Package::Packages(l.to_vec()).partial_cmp(&Package::Packages(vec![Package::Number(r.to_owned())]))
            },
            (Package::Packages(ll), Package::Packages(rr)) => {
                let len_l = ll.len();
                let len_r = rr.len();
                let results = zip(ll, rr)
                .map(|(l, r)| l.partial_cmp(r).unwrap())
                .filter(|&x| x != Ordering::Equal)
                .collect::<Vec<Ordering>>();
                if !results.is_empty() {
                    return Some(results[0]);
                }
                if len_l < len_r {
                    Some(Ordering::Less)
                } else if len_l == len_r {
                    Some(Ordering::Equal)
                } else {
                    Some(Ordering::Greater)
                }
            },
        }
    }
}

impl Ord for Package {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

fn part1(input: &str) -> u32 {
    let mut tot: u32 = 0;
    for (i, pair) in input.split("\n\n").enumerate() {
        let mut lines = pair.lines();
        let l: Value = serde_json::from_str(lines.next().unwrap()).unwrap();
        let r: Value = serde_json::from_str(lines.next().unwrap()).unwrap();
        if Package::try_from(&l).unwrap() < Package::try_from(&r).unwrap() {
            tot += (i as u32)+1;
        }
    }
    tot
}


fn part2(input: &str) -> u32 {
    let v_2: Value = serde_json::from_str("[[2]]").unwrap();
    let v_6: Value = serde_json::from_str("[[6]]").unwrap();
    let p2 = Package::try_from(&v_2).unwrap();
    let p6 = Package::try_from(&v_6).unwrap();
    let mut res: u32 = 1;

    let mut packages = input.split('\n')
        .filter(|&l| !l.is_empty() )
        .map(|l| serde_json::from_str(l).unwrap())
        .collect::<Vec<Value>>()
        .iter().map(|v| Package::try_from(v).unwrap())
        .collect::<Vec<Package>>();
    packages.push(p2);
    packages.push(p6);
    packages.sort();
    let p2 = Package::try_from(&v_2).unwrap();
    let p6 = Package::try_from(&v_6).unwrap();

    for (i, p) in packages.iter().enumerate() {
        if p == &p2 {
            res *= (i as u32) + 1;
        }
        if p == &p6 {
            res *= (i as u32) + 1;
        }
    }
    res
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
    use serde_json::Value;
    use crate::{Package, part1, part2};
    use std::iter::zip;

    #[test]
    fn test_compare(){
        let left = ["[1,1,3,1,1]", "[[1],[2,3,4]]", "[9]", "[[4,4],4,4]", "[7,7,7,7]", "[]", "[[[]]]", "[1,[2,[3,[4,[5,6,7]]]],8,9]"];
        let right = ["[1,1,5,1,1]", "[[1],4]", "[[8,7,6]]", "[[4,4],4,4,4]", "[7,7,7]", "[3]", "[[]]", "[1,[2,[3,[4,[5,6,0]]]],8,9]"];
        let v_left = left.map(|l| serde_json::from_str(l).unwrap());
        let val_left: Vec<&Value> = v_left.iter().collect();
        let v_right = right.map(|r| serde_json::from_str(r).unwrap());
        let val_right: Vec<&Value> = v_right.iter().collect();
        let res = zip(val_left, val_right).map(|(l, r)| Package::try_from(l).unwrap() <  Package::try_from(r).unwrap()).collect::<Vec<bool>>();
        assert_eq!(res, vec![true, true, false, true, false, true, false, false]);
    }

    #[test]
    fn test_part1(){
        let input = include_str!("../test").trim();
        let res = part1(input);
        assert_eq!(res, 13);
    }


    #[test]
    fn test_part2(){
        let input = include_str!("../test").trim();
        let res = part2(input);
        assert_eq!(res, 140);
    }
}