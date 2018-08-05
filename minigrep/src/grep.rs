use std::error::Error;
use std::fs::File;
use std::io::Read;

#[derive(Debug)]
pub struct Config { 
    query: String, 
    filename: String, 
    case_sensitive: bool 
}

impl Config {
    pub fn new(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = args[1].clone();
        let filename = args[2].clone();
        let case_sensitive = args[3].clone() != "insensitive";

        Ok(Config { query, filename, case_sensitive })
    }

    pub fn run<'a>(config: Config) -> Result<Vec<(usize, String)>, Box<Error>> {
        let contents = read_file(&config.filename)?;  
        // 🚕🚕🚕🚕
        let results = if config.case_sensitive {
            search_case_sensitive(&config.query, &contents)
        } else {
            search_case_insensitive(&config.query, &contents)
        };

        let results: Vec<_> = results.into_iter().map(|(u, r)| (u, String::from(r))).collect();

        Ok(results)
    }
}

fn read_file(filename: &str) -> Result<String, Box<Error>> {
    let mut file = File::open(filename)?;
    let mut content = String::new();
    file.read_to_string(&mut content)?;
    return Ok(content)
}

fn search_case_sensitive<'a>(query: &str, content: &'a str) -> Vec<(usize, &'a str)> {
    content.lines().enumerate().filter(|&(_, line)| line.contains(query)).collect()
}

fn search_case_insensitive<'a>(query: &str, content: &'a str) -> Vec<(usize, &'a str)> {
    let query = query.to_lowercase();
    content.lines().enumerate().filter(|&(_, line)| line.to_lowercase().contains(&query)).collect()
}


#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn case_sensitive() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.
Duct tape.";

        assert_eq!(
            "safe, fast, productive.",
            super::search_case_sensitive(query, contents)[0].1
        );

        let query = "nothing!";
        assert_eq!(0, search_case_sensitive(query, contents).len());
    }

    #[test]
    fn case_insensitive() {
        let query = "rUsT";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.
Trust me.";

        assert_eq!(
            "Rust:",
            search_case_insensitive(query, contents)[0].1
        );

        let query = "nothing!";
        assert_eq!(0, search_case_insensitive(query, contents).len());
    }
}
