use serde_json::Value;
use std::iter::zip;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
enum CompValue {
    Left,
    Right,
    Undecided,
}

fn compare(left: &Value, right: &Value) -> Result<CompValue, ()> {
    match (left, right) {
        (Value::Number(l), Value::Number(r)) => {
            if l.as_u64() < r.as_u64() {
                Ok(CompValue::Left)
            } else if l == r {
                Ok(CompValue::Undecided)
            } else {
                Ok(CompValue::Right)
            }
        },
        (Value::Number(l), Value::Array(r)) => {
            compare(&Value::Array(vec![Value::Number(l.to_owned())]), &Value::Array(r.to_vec()))
        },
        (Value::Array(l), Value::Number(r)) => {
            compare(&Value::Array(l.to_vec()), &Value::Array(vec![Value::Number(r.to_owned())]))
        },
        (Value::Array(ll), Value::Array(rr)) => {
            let len_l = ll.len();
            let len_r = rr.len();
            let results = zip(ll, rr)
            .map(|(l, r)| compare(l, r).unwrap())
            .filter(|res| res != &CompValue::Undecided).collect::<Vec<CompValue>>();
            if !results.is_empty() {
                return Ok(results[0]);
            }
            if len_l < len_r {
                Ok(CompValue::Left)
            } else if len_l == len_r {
                Ok(CompValue::Undecided)
            } else {
                Ok(CompValue::Right)
            }
        },
        _ => {Err(())},
    }
}


fn part1(input: &str) -> u32 {
    let mut tot: u32 = 0;
    for (i, pair) in input.split("\n\n").enumerate() {
        let mut lines = pair.lines();
        let l: Value = serde_json::from_str(lines.next().unwrap()).unwrap();
        let r: Value = serde_json::from_str(lines.next().unwrap()).unwrap();
        if compare(&l, &r).unwrap() == CompValue::Left {
            tot += (i as u32)+1;
        }
    }
    tot
}


fn main() {
        
    let path_st = Path::new("status");

    let input = include_str!("../input").trim();
    let res_1 = part1(input);
    //let res_2 = part2(input);
    
    let path_o1 = Path::new("output1");
    let mut file = File::create(path_o1).unwrap();
    file.write_all(format!("{res_1}").as_bytes()).unwrap();

    let mut file = File::create(path_st).unwrap();
    file.write_all("1\n".as_bytes()).unwrap();
}

#[cfg(test)]
mod test {
    use serde_json::Value;
    use crate::{CompValue, compare, part1};
    use std::iter::zip;

    #[test]
    fn test_compare(){
        let left = ["[1,1,3,1,1]", "[[1],[2,3,4]]", "[9]", "[[4,4],4,4]", "[7,7,7,7]", "[]", "[[[]]]", "[1,[2,[3,[4,[5,6,7]]]],8,9]"];
        let right = ["[1,1,5,1,1]", "[[1],4]", "[[8,7,6]]", "[[4,4],4,4,4]", "[7,7,7]", "[3]", "[[]]", "[1,[2,[3,[4,[5,6,0]]]],8,9]"];
        let v_left = left.map(|l| serde_json::from_str(l).unwrap());
        let val_left: Vec<&Value> = v_left.iter().collect();
        let v_right = right.map(|r| serde_json::from_str(r).unwrap());
        let val_right: Vec<&Value> = v_right.iter().collect();
        let res = zip(val_left, val_right).map(|(l, r)| compare(l, r).unwrap()).collect::<Vec<CompValue>>();
        assert_eq!(res, vec![CompValue::Left, CompValue::Left, CompValue::Right, CompValue::Left, CompValue::Right, CompValue::Left, CompValue::Right, CompValue::Right]);
    }

    #[test]
    fn test_part1(){
        let input = include_str!("../test").trim();
        let res = part1(input);
        assert_eq!(res, 13);
    }
}