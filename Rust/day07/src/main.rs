use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use std::collections::HashMap;

fn child(path: &str, dir: &str) -> String {
    let mut p = String::from(path);
    p.push('/');
    p.push_str(dir);
    p
}


fn parent(path: &str) -> String {
    let mut ps = path.split('/').collect::<Vec<&str>>();
    ps.pop();
    ps.join("/")
}

fn dir_tree(directory: &str) -> Vec<String> {
    if directory == String::from("") {
        return vec![String::from("")];
    }
    let mut tree: Vec<String> = Vec::new();
    let dirs = directory.split('/').collect::<Vec<&str>>();
    for i in 1..dirs.len()+1 {
        let d = dirs[0..i].join("/");
        tree.push(d);
    }
    tree
}

fn filesystem(input: String) -> HashMap<String, u128> {
    let mut files: HashMap<String, u128> = HashMap::new();
    files.insert(String::from(""), 0);
    let mut cwd = String::from("");
    let mut tree = vec![String::from("")];
    let commands = input.split('\n').collect::<Vec<&str>>();
    for i in 1..commands.len() {
        let command = commands[i];
        if command == "$ cd .." {
            cwd = parent(&cwd);
            tree = dir_tree(&cwd);
        } else if command.starts_with("$ cd ") {
            cwd = child(&cwd, command.split_at(5).1);
            tree = dir_tree(&cwd);
        } else if command.starts_with("dir ") {
            files.insert(child(&cwd, command.split_at(4).1), 0);
        } else if !command.starts_with("$") {
            let size = command.split(' ').collect::<Vec<&str>>()[0].parse::<u128>().unwrap();
            for d in tree.clone() {
                files.insert(d.clone(), files.get(&d).unwrap()+size);
            }
        }
    }
    files
}

fn part1(input: String) -> u128 {
    let fs = filesystem(input);
    let mut tot: u128 = 0;
    for v in fs.values() {
        let v2 = v.to_owned();
        if v2 < 100000{
            tot += v2;
        }
    }
    tot
}

fn main() {
        
    let path_st = Path::new("status");

    let input = include_str!("../input").trim();
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
    fn paths(){
        assert_eq!(crate::parent("/a/b"), String::from("/a"));
        assert_eq!(crate::parent("/a"), String::from(""));
        assert_eq!(crate::child("", "a"), String::from("/a"));
        assert_eq!(crate::child("/a", "b"), String::from("/a/b"));
        assert_eq!(crate::dir_tree("/a/b"), vec![String::from(""), String::from("/a"), String::from("/a/b")]);
    }

    #[test]
    fn test_part1(){
        let input = include_str!("../test").trim();
        let res = crate::part1(String::from(input));
        assert_eq!(res, 95437);
    }
}