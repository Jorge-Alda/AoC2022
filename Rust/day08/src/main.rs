use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use itertools::Itertools;

fn part1(input: String) -> usize {
    let rows = input.split('\n').collect::<Vec<&str>>();
    let trees = rows.iter().map(|r| r.chars().collect::<Vec<char>>()).collect::<Vec<Vec<char>>>();
    let n_rows = rows.len();
    let n_cols = rows[0].len();

    let mut v_left = vec![vec![true; n_cols]; n_rows];
    let mut v_right = vec![vec![true; n_cols]; n_rows];
    let mut v_top = vec![vec![true; n_cols]; n_rows];
    let mut v_bottom = vec![vec![true; n_cols]; n_rows];

    for i in 0..n_rows {
        for j in 1..n_cols {
            v_left[i][j] = (0..j)
                .all(|k| trees[i][j] > trees[i][k]);
            v_right[i][n_cols-j-1] = (0..j)
                .all(|k| trees[i][n_cols-j-1] > trees[i][n_cols-k-1]);
        }
    }

    for j in 0..n_cols {
        for i in 1..n_cols {
            v_top[i][j] = (0..i)
                .all(|k| trees[i][j] > trees[k][j]);
            v_bottom[n_rows-i-1][j] = (0..i)
                .all(|k| trees[n_rows-i-1][j] > trees[n_rows-k-1][j]);
        }
    }

    (0..n_rows)
        .cartesian_product(0..n_cols)
        .filter(|(i, j)| v_left[*i][*j] || v_right[*i][*j] || v_top[*i][*j] || v_bottom[*i][*j])
        .count()
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
mod test {
    #[test]
    fn test_part1(){
        let input = include_str!("../test").trim();
        let res = crate::part1(String::from(input));
        assert_eq!(res, 21);
    }
}
