use std::collections::VecDeque;
use std::convert::From;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;


#[derive(Debug,PartialEq,Eq,Clone)]
enum Operations {
    Sum(u128),
    Mult(u128),
    Square,
}


impl From<&str> for Operations {
    fn from(op: &str) -> Self {
        if op == "* old" {
            return Operations::Square;
        } else if op.starts_with("+ ") {
            let x: u128 = op[2..op.len()].parse().unwrap();
            return Operations::Sum(x);
        } else {
            let x: u128 = op[2..op.len()].parse().unwrap();
            return Operations::Mult(x);
        }
    }
}


#[derive(Debug, Clone)]
struct Monkey {
    items: VecDeque<u128>,
    operation: Operations,
    test: u128,
    throw_true: usize,
    throw_false: usize,
    inspected: u64,
}

impl From<&str> for Monkey {
    fn from(descr: &str) -> Self {
        let mut lines = descr.split('\n').collect::<VecDeque<&str>>();
        lines.pop_front();
        let items = lines.pop_front().unwrap()
            .strip_prefix("  Starting items: ").unwrap()
            .split(", ")
            .map(|x| x.parse::<u128>().unwrap())
            .collect::<VecDeque<u128>>();
        let operation = Operations::from(lines.pop_front().unwrap().strip_prefix("  Operation: new = old ").unwrap());
        let test: u128 = lines.pop_front().unwrap()
            .strip_prefix("  Test: divisible by ").unwrap()
            .parse().unwrap();
        let throw_true: usize = lines.pop_front().unwrap()
            .strip_prefix("    If true: throw to monkey ").unwrap()
            .parse().unwrap();
        let throw_false: usize = lines.pop_front().unwrap()
                .strip_prefix("    If false: throw to monkey ").unwrap()
                .parse().unwrap();
        Monkey { items, operation, test, throw_true, throw_false, inspected: 0 }
    }
}

impl Monkey {
    fn append(&mut self, item: u128) {
        self.items.push_back(item);
    }

    fn process_item(&mut self, d: u128, masterdiv: u128) -> (usize, u128) {
        let item = self.items.pop_front().unwrap();
        let worry = match self.operation {
            Operations::Square => (item.pow(2) / d) % masterdiv,
            Operations::Mult(x) => ((item * x) / d) % masterdiv,
            Operations::Sum(x) => ((item + x) / d) % masterdiv,
        };
        self.inspected += 1;
        if worry % self.test == 0 {
            return (self.throw_true, worry);
        } else {
            return (self.throw_false, worry);
        }
    }
}

fn solve(input: &str, d: u128, rounds: u64) -> u64 {
    let mut monkeys = input.split("\n\n")
        .map(|l| Monkey::from(l))
        .collect::<Vec<Monkey>>();

    let masterdiv = monkeys.iter()
        .map(|x| x.test)
        .reduce(|x, y| x*y).unwrap();

    for _ in 0..rounds {
        for i in 0..monkeys.len() {
            while monkeys[i].items.len() > 0 {
                let (t, w) = monkeys[i].process_item(d, masterdiv);
                monkeys[t].append(w);
            }
        }
    }

    let mut max1: u64 = 0;
    let mut max2: u64 = 0;
    for m in monkeys {
        if m.inspected > max1 {
            max2 = max1;
            max1 = m.inspected;
        } else if m.inspected > max2 {
            max2 = m.inspected;
        }
    }
    max1 * max2
}


fn main() {
        
    let path_st = Path::new("status");

    let input = include_str!("../input").trim();
    let res_1 = solve(input, 3, 20);
    let res_2 = solve(input, 1, 10000);
    
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
mod tests {
    #[test]
    fn part_1() {
        let input = include_str!("../test").trim();
        let res = crate::solve(input, 3, 20);
        assert_eq!(res, 10605);
    }

    #[test]
    fn part_2() {
        let input = include_str!("../test").trim();
        let res = crate::solve(input, 1, 10000);
        assert_eq!(res, 2713310158);
    }
}