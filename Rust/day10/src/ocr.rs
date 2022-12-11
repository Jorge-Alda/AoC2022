use itertools::Itertools;


#[derive(Debug)]
pub enum OcrError {
    UnknownLetter(String),
    WrongNumberLines(usize),
    WrongWidth(usize),
    MismatchedWidth,
}

fn parse_letter(l: &str) -> Result<char, OcrError> {
    match l {
        " ## \n#  #\n#  #\n####\n#  #\n#  #" => Ok('A'),
        "### \n#  #\n### \n#  #\n#  #\n### " => Ok('B'),
        " ## \n#  #\n#   \n#   \n#  #\n ## " => Ok('C'),
        "####\n#   \n### \n#   \n#   \n####" => Ok('E'),
        "####\n#   \n### \n#   \n#   \n#   " => Ok('F'),
        " ## \n#  #\n#   \n# ##\n#  #\n ###" => Ok('G'),
        "#  #\n#  #\n####\n#  #\n#  #\n#  #" => Ok('H'),
        " ###\n  # \n  # \n  # \n  # \n ###" => Ok('I'),
        "  ##\n   #\n   #\n   #\n#  #\n ## " => Ok('J'),
        "#  #\n# # \n##  \n# # \n# # \n#  #" => Ok('K'),
        "#   \n#   \n#   \n#   \n#   \n####" => Ok('L'),
        " ## \n#  #\n#  #\n#  #\n#  #\n ## " => Ok('O'),
        "### \n#  #\n#  #\n### \n#   \n#   " => Ok('P'),
        "### \n#  #\n#  #\n### \n# # \n#  #" => Ok('R'),
        " ###\n#   \n#   \n ## \n   #\n### " => Ok('S'),
        "#  #\n#  #\n#  #\n#  #\n#  #\n ## " => Ok('U'),
        "#   \n#   \n # #\n  # \n  # \n  # " => Ok('Y'),
        "####\n   #\n  # \n #  \n#   \n####" => Ok('Z'),
        _ => Err(OcrError::UnknownLetter(String::from(l))),
    }
}

pub fn ocr_scan(input: String) -> Result<String, OcrError> {
    let mut word = String::new();
    let lines = input.split('\n').collect::<Vec<&str>>();
    if lines.len() != 6 {
        return Err(OcrError::WrongNumberLines(lines.len()));
    }
    let width = lines[0].len();
    if width % 5 != 0 {
        return Err(OcrError::WrongWidth(width));
    }
    if lines.iter().any(|&x| x.len() != width) {
        return Err(OcrError::MismatchedWidth);
    }
    for i in 0..(width/5) {
        let c = lines
            .iter()
            .map(|x| &x[(5*i)..(5*i+4)])
            .join("\n");
        let letter = parse_letter(&c);
        match letter {
            Ok(a) => {word.push(a);},
            Err(e) => {return Err(e);}
        }
    }
    Ok(word)
}

#[test]
fn test_ocr(){
    assert_eq!(ocr_scan(String::from(" ##  \n#  # \n#  # \n#### \n#  # \n#  # ")).unwrap(), String::from("A"));
}