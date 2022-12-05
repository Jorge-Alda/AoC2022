use std::fs::File;
use std::io::prelude::*;
use std::path::Path;


struct ParsedInput {
    crates: Vec<String>,
    instructions: Vec<String>,
}

fn parse(input: String) -> ParsedInput {
    let input_s: Vec<&str> = input.split("\n\n").collect();
    let mut cr: Vec<&str> = input_s[0].split('\n').collect();
    let instructions: Vec<String> = input_s[1].trim().split('\n').map(|x| String::from(x)).collect();

    let containers: Vec<&str> = cr.pop().unwrap().split_whitespace().collect();
    let len: usize = containers.last().unwrap().parse().unwrap();

    let mut crates: Vec<String> = Vec::new();

    for _i in 0..len {
        crates.push(String::from(""));
    }

    for c in cr {
        for i in 0..len {
            let ind = 4*i+1;
            if c.len() > ind {
                let x = c.chars().nth(ind).unwrap();
                if x != ' ' {
                    crates[i].push(x);
                }
            }
        }
    }

    ParsedInput {crates, instructions }
}

fn move_1by1 (crates: &mut Vec<String>, source: usize, dest: usize, quant: usize){
    let s = crates[source].clone();
    let (moved, remain) = s.split_at(quant);

    let mut moved_v: Vec<char> = moved.chars().collect();
    moved_v.reverse();
    let mut received = String::from("");
    received.extend(moved_v);

    received.push_str(crates[dest].as_str());
    crates[dest] = received;
    crates[source] = String::from(remain);
}

fn part1 (input: String) -> String {
    let parsed = parse(input);
    let mut crates = parsed.crates.clone();
    for ins in parsed.instructions {
        let ins_s: Vec<&str> = ins.split_whitespace().collect();
        let quant: usize = ins_s[1].parse().unwrap();
        let mut source: usize = ins_s[3].parse().unwrap();
        let mut dest: usize = ins_s[5].parse().unwrap();
        source -= 1;
        dest -= 1;
        move_1by1(&mut crates, source, dest, quant);
    }
    let mut res = String::from("");
    for c in crates {
        res.push(c.chars().nth(0).unwrap());
    }
    res
}

fn main() {
        
    let path_st = Path::new("status");

    let input = include_str!("../input");
    let res = crate::part1(String::from(input));
    
    let path_o1 = Path::new("output1");
    let mut file = File::create(path_o1).unwrap();
    file.write_all(format!("{res}").as_bytes()).unwrap();

    let mut file = File::create(path_st).unwrap();
    file.write_all("1\n".as_bytes()).unwrap();

}

#[cfg(test)]
mod tests {
    #[test]
    fn test_part1(){
        let input = include_str!("../test");
        let res = crate::part1(String::from(input));
        assert_eq!(res, String::from("CMZ"));
    }

    //#[test]
    //fn test_part2(){
    //    let input = include_str!("../test");
    //    let res = crate::part2(String::from(input.trim()));
    //    assert_eq!(res, 4);
    //}
}