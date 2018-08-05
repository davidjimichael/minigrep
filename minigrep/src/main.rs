extern crate minigrep;

use std::env;
use minigrep::grep::Config;
use minigrep::cache;

fn main() {
    let args: Vec<_> = env::args().collect();
    let config = Config::new(&args).expect("nan");
    
    println!("Searching for {}", &args[1]);
    println!("In file {}", &args[2]);

    match Config::run(config) {
        Ok(results) => {
            for (num, line) in results {
                // display misaligned when i > 9
                println!("   |\n{}  | {}\n   |\n", num, line);
            }
        },
        Err(e) => eprintln!("ERROR: {}", e),
    } 

    // ----- testing caching ---------

    // this function will always return one
    let mut _cache = cache::Cacher::new(|_x| 1);
    assert_eq!(_cache.value(10), 1);

}
